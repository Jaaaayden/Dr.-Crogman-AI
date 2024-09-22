from openai import OpenAI 
import time

client: OpenAI = OpenAI()

assistant: OpenAI = client.beta.assistants.create(
    name="Horace Crogman",
    instructions=
    """
    You are Dr. Horace Crogman, a physics professor at California State University: Dominguez Hills 
    You speak with all lowercase, ellipses, and grammatical errors; use 1-2 sentences max per response.
    Running a program called 'CSUDH MSEIP-STALP', and addressing participants of this program.
    When presented with a difficult-to-answer question, always take a side instead of saying it's subjective.
    Some facts about you include you:
    You dislike comedy clubs as comedians usually mock their audiences; you’d sit in the back and hide.
    You strongly discourage eating meat; you are vegan.
    You see potential in VR and AI.  
    You believe evolution isn't real. 
    You grew up in a Rastafarian household.
    You advocate for North Korea having nukes.
    """,
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-0125",   
)

thread: OpenAI = client.beta.threads.create()
print(thread)

def get_response(user_input: str, username: str, channel: str) -> str:
    if (channel != 'general' and ('<@1262816977303638036>' in user_input or '<@&1262817729761644547>' in user_input)):
        # Lowercase everything because Python is case-sensitive
        lowered = user_input.lower()
        
        message = client.beta.threads.messages.create(
            thread_id = thread.id,
            role = 'user',
            content = f"{lowered}",
        )
        
        run = client.beta.threads.runs.create(
            thread_id = thread.id,
            assistant_id = assistant.id,
        )
        
        while run.status != 'completed':
            run = client.beta.threads.runs.retrieve(
                thread_id = thread.id,
                run_id = run.id,
            )
            time.sleep(1)
            
        messages: list = client.beta.threads.messages.list(
            thread_id = thread.id,
        )
        
        response: list = []
        
        for message in reversed(messages.data):
            response.append(message.content[0].text.value)
        print(response[len(response) - 1])
        return response[len(response) - 1]
