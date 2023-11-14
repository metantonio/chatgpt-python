import os
import openai
import csv
import requests

openai.api_key = os.environ.get("OPENAI_API_KEY")

# models
test_model = {"name": "text-davinci-003", "tokens": 2048}
chatgpt_3 = {"name": "gpt-3.5-turbo", "tokens": 4096}
chatgpt_4 = {"name": "gpt-4-1106-preview", "tokens": 128000}

#Select Model to use:
model_selected = chatgpt_4

#path to .csv files
csv_directory  = './csv'

def menuOptions():
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
    userOp = int(input("\n Choose an option \n"))
    return userOp

def menuFunctions(user):
    if(user==1):
        prompt = input("\n Write a prompt to ChatGPT\n \n")

        completation = openai.Completion.create(
            engine=model_selected["name"], prompt=prompt, n=1, max_tokens=model_selected["tokens"]
        )

        print(completation.choices[0].text)
    if(user==2):
        print("Reading .csv file")
        # Loop over directory files
        for filename in os.listdir(csv_directory):
            if filename.endswith('.csv'):
                # create the path to file
                csv_file_path = os.path.join(csv_directory, filename)
                
                # open the .csv file in read-only mode
                with open(csv_file_path, mode='r') as file:
                    # create a reader of the headers
                    csv_reader = csv.DictReader(file)
                    
                    # name of the columns
                    existing_columns = csv_reader.fieldnames

                    # add a new column at the end, for the response of chatGPT
                    new_columns = existing_columns + ['chatgpt']

                    # Crea a new file that will contain the response of server
                    output_csv_path = os.path.join(csv_directory, f"output_{filename}")

                    with open(output_csv_path, mode='w', newline='') as output_file:
                        csv_writer = csv.DictWriter(output_file, fieldnames=new_columns)
                        csv_writer.writeheader()

                        # loop every row
                        for row in csv_reader:
                            # obtain columns with certain header                      
                            name = row['casinoName']
                            address = row['address'].replace('\n', '').replace('\r', '').replace('\t', '').replace('  ', '')
                            
                            prompt = f'With following casino named: {name} with address {address} try to retrieve the information of the restaurants inside of the property. If there is not any restaurante then give me the nearest to it'
                            # change if necessary
                            print(prompt)
                            completation = openai.Completion.create(
                                engine=model_selected["name"], prompt=prompt, n=1, max_tokens=model_selected["tokens"]
                            )

                            #print(completation.choices[0].text)
                            #add the response
                            row['server_response'] = completation.choices[0].text

                            # write the output file
                            csv_writer.writerow(row)

                    print("Process ended")


if __name__ == "__main__":
    
    userOp1 = menuOptions()

    while userOp1 < 3:
        
        menuFunctions(userOp1)
        userOp1 = menuOptions()

        if userOp1 >= 3:
            print('Closing Script')
            break
