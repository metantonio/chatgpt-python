import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

# models
test_model = {"name": "text-davinci-003", "tokens": 2048}
chatgpt_3 = {"name": "gpt-3.5-turbo", "tokens": 4096}
chatgpt_4 = {"name": "gpt-4-1106-preview", "tokens": 128000}

#Select Model to use:
model_selected = chatgpt_4

if __name__ == "__main__":
    print(
        """\n Main Menu

    Menú:

    
    1-. Prompting from console
    2-. Read a .csv file and run a custom prompting
    3-. Exit

    Script: Antonio Martínez
    @metantonio
    """
    )
    userOp1 = int(input("\n Choose an option \n"))

    while userOp1 < 3:
        prompt = input("\n Introduce el prompt a chatgpt-3 o 'exit' para salir\n \n")

        if prompt == "exit":
            break

        completation = openai.Completion.create(
            engine=model_selected["name"], prompt=prompt, n=1, max_tokens=model_selected["tokens"]
        )

        print(completation.choices[0].text)

        userOp1 = int(input("\n Choose an option \n"))

        if userOp1>=3:
            print('Closing Script')
            break
