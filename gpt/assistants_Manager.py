import openai
import json

from gpt.assistants_functions import FUNCTIONS, FUNCTIONS_MAP

def is_valid_openai_key(key):
    try:
        openai.api_key = key
        openai.models.list()
        return True
    except Exception as e:
        return False

class AssistantManager:    
    def __init__(self, api_key):
        self._client = openai.OpenAI(api_key=api_key)
        self._assistants = self._create_assistant()
        self._thread = None
        self._run = None
        
    def _create_assistant(self):
        return self._client.beta.assistants.create(
            name="Research Assistant",
            instructions="""
            Use the provided tool to answer the user's question.
            The user's question requires you to use a tool to find information. Use either 'wikipedia_search_tool' or 'duckduckgo_search_tool' as needed.
            If what you find has a 'URL', go to the website and answer with an excerpt from the website.
            """,
            model="gpt-4o",
            tools=FUNCTIONS
        )
        
    def _create_thread(self, contents):
        return self._client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": contents,
                }
            ]
        )
        
    def _create_run(self):
        return self._client.beta.threads.runs.create_and_poll(
            thread_id=self._thread.id,
            assistant_id=self._assistants.id,
        )
        
    def get_run(self):
        return self._client.beta.threads.runs.retrieve(thread_id=self._thread.id, run_id=self._run.id)
    
    def research_topic(self, content):
        self._thread = self._create_thread(content)
        self._run = self._create_run()
        
    def get_messages(self):
        messages = self._client.beta.threads.messages.list(thread_id=self._thread.id)
        messages = list(messages)
        messages.reverse()
        assistant_message = None
        for message in messages:
            if message.role == "assistant":
                assistant_message = message.content[0].text.value
        return assistant_message
    
    def _get_tool_outputs(self):
        outputs = []
        self._run = self.get_run()
        for action in self._run.required_action.submit_tool_outputs.tool_calls:
            action_id = action.id
            function = action.function
            if function.name in FUNCTIONS_MAP:
                outputs.append(
                    {
                        "tool_call_id": action_id,
                        "output": FUNCTIONS_MAP[function.name](json.loads(function.arguments))
                    }
                )
            else:
                outputs.append(
                    {
                        "tool_call_id": action_id,
                        "output": "Function not found.",
                    }
                )
        return outputs
    
    def submit_tool_outputs(self):
        outputs = self._get_tool_outputs()
        return self._client.beta.threads.runs.submit_tool_outputs_and_poll(
            run_id=self._run.id,
            thread_id=self._thread.id,
            tool_outputs=outputs,
        )
    
    def runs_poll(self):
        self._client.beta.threads.runs.poll(thread_id=self._thread.id, run_id=self._run.id)
