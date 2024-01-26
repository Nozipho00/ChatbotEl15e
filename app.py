from http import client
import json
from urllib import request, response
import streamlit as st
import requests
from io import BytesIO
import os
import boto3
import base64



st.set_page_config(page_title="AskEL15e", page_icon="OMU.JO-4aa2b32b.png", layout="wide")

# st.title("AskEL15")

# pdf_upload = st.file_uploader("Upload Document", type=["pdf"])

#****Upload pdf to S3

post_api_gateway_url = 'https://t28j1zf0cb.execute-api.us-east-1.amazonaws.com/dev/uploader'



def upload_file_to_lambda(file_content_base64, post_api_gateway_url):
    try:
        # Make an HTTP request to the API Gateway endpoint
        response = requests.post(post_api_gateway_url, json={'body': file_content_base64})

        return response.status_code, response.text
    except Exception as e:
        return 500, str(e)

response_placeholder = st.empty()

def main():
    st.title("AskEL15e")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])



    if uploaded_file is not None:
        if st.button("Upload File"):
            # Encode the file content in base64
            file_content_base64 = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

            post_api_gateway_url = 'https://t28j1zf0cb.execute-api.us-east-1.amazonaws.com/dev/uploader'
            status_code, response_text = upload_file_to_lambda(file_content_base64, post_api_gateway_url)

            if status_code == 200:
                st.success(f"File uploaded successfully. Response: {response_text}")
            else:
                st.error(f"Error uploading file. Status code: {status_code}, Response: {response_text}")



if __name__ == "__main__":
    main()


# if st.button("Process"):
#     if pdf_upload is not None:
#         pdf_details = {"filename":pdf_upload.name,"filetype":pdf_upload.type}

#     with st.spinner("Processing..."):


#         def upload_file_to_lambda(file_path):
#             try:
#                 with open(file_path, 'rb') as file:
#             # Encode the file content in base64
#                     file_content_base64 = base64.b64encode(file.read()).decode('utf-8')

#         # Make an HTTP request to the API Gateway endpoint
#                 response = requests.post(api_gateway_url, json={'body': file_content_base64})

#         # Check the response status code
#                 if response.status_code == 200:
#                     st.success("File uploaded successfully")
#                 else:
#                     st.error(f"Error uploading file. Status code: {response.status_code}, Response: {response.text}")
#             except Exception as e:
#                     st.error(f"Error uploading file: {str(e)}")

# # Streamlit UI
# st.title("Upload PDF to S3 via Lambda and API Gateway")
# uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# if uploaded_file is not None:
#     if st.button("Upload File"):
#         # Save the uploaded file to a temporary location
#         with open("temp.pdf", "wb") as temp_file:
#             temp_file.write(uploaded_file.getvalue())
#         # Upload the file to Lambda via API Gateway
#         upload_file_to_lambda("temp.pdf")


       #loads data into the s3 doesn't use the lambda ****
        # bucket = 'om-hackathon-context-store'

        # pdf_contents = pdf_upload.read()

        # # Assuming you are using AWS S3
        # s3 = boto3.client('s3')

        # # Upload the file to the specified S3 bucket
        # s3.upload_fileobj(pdf_upload, bucket, pdf_upload.name)

        # st.success("File uploaded successfully.")
        #****

        # data = open (pdf_upload, 'rb')

        # client.upload_file(pdf_upload, bucket)
        
        # api_gateway_endpoint = "https://bcsehqea2jojca366niuilfbhy0mdopu.lambda-url.us-east-1.on.aws/"
        # s3_object_name = f"s3://om-hackathon-context-store/"
        
        # with BytesIO(pdf_upload.read()) as file_content:
        #     files = {'file': (s3_object_name, file_content)}
        #     response = requests.post(api_gateway_endpoint, files=files)

        # if response.status_code == 200:
        #     st.success("File uploaded successfully!")
        # else:
        #     st.error(f"Error uploading file: {response.text}")
    # if pdf_upload.type != "application/pdf":
    #         st.text("Please Upload a PDF file.")

#*** chatbot interaction 
get_api_gateway_url = 'https://nbfe0cxv70.execute-api.us-east-1.amazonaws.com/dev/dialog-engine'


if "messages" not in st.session_state:
    st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input("How can I assist you ?")

def get_lambda_response(prompt):
    lambda_client = boto3.client("lambda", region_name="us-east-1")
    result = ""

    # Construct payload for the Lambda function
    payload = {
        "prompt": prompt,
    }

    # Call the Lambda function
    response = lambda_client.invoke(
        FunctionName="dialog-engine",  # Replace with your Lambda function name
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )


    # Extract and return the response
    result = json.loads(response["Payload"].read())

    

    # Update the response in the Streamlit UI
    response_placeholder.text(result["body"])
    return result["body"]



if prompt:

    with st.chat_message("user"):
        if st.markdown(prompt):
            response = get_lambda_response(prompt)

    with st.chat_message("assistant"):
            st.markdown(response)
            # st.text("Response")
            # st.write(response)

    # st.session_state.messages.append({"role": "user", "content": prompt})






    # with st.chat_message("user"):
    #     st.markdown(prompt)

    # st.session_state.messages.append({"role": "user", "content": prompt})
















    # content  =  st.chat_message("content")
    # response = requests.post(get_api_gateway_url, json=content)

# response = f"Echo: {prompt}"

# with st.chat_message("assistant"):
#            st.markdown(response)

# st.session_state.messages.append({"role": "assistant", "content": response})

    #This is where the magic happens 

  #  with st.chat_message("assistant"):
  #   message_placeholder = st.empty()
  #      full_response =  ""
   #     for response in 






