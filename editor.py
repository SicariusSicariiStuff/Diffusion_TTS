import gradio as gr
import json

def create_conversation_pair(question_text, answer_text):
    # Split the strings into lines assuming each line is a separate question or answer
    question_strings = question_text.strip().split('\n')
    answer_strings = answer_text.strip().split('\n')

    # Ensure the lengths of question_strings and answer_strings are the same
    min_length = min(len(question_strings), len(answer_strings))

    # Create conversation pairs
    conversations = []

    for i in range(min_length):
        # Create conversation pair
        conversation_pair = [
            {"from": "human", "value": question_strings[i]},
            {"from": "gpt", "value": answer_strings[i]}
        ]

        conversations.append(conversation_pair)

    return conversations

# Gradio GUI
with gr.Blocks() as User_Interface_GUI:
    with gr.Row():
        with gr.Column():
            question_text_field = gr.components.Textbox(label="Question", lines=4, interactive=True)
            answer_text_field = gr.components.Textbox(label="Answer", lines=15, interactive=True)
            with gr.Row():
                index_write_decision = gr.components.Radio(choices=["Create new index", "Add to the last index"],
                                                           label="JSON Creation", value="Create new index",
                                                           interactive=True)
                conversation_id_record = gr.Number(label="Conversation ID:",
                                                   value=1, minimum=1, interactive=True)
                output_filename = gr.components.Textbox(label=["Filename"],
                                                        value='shareGPT.json', interactive=True)
            with gr.Column():
                save_json_shareGPT = gr.components.Button(value="Save")

        with gr.Column():
            output_text_field = gr.components.Textbox(label="Output", lines=34)
            #
            # ============Functions start here============
            def on_save_button_click(question_text,answer_text,filename_text,id_text):



                conversations = create_conversation_pair(question_text, answer_text)

                # Create JSON structure
                json_structure = [{"id": int(id_text), "conversations": conversation} for i, conversation in enumerate(conversations, 1)]

                # Export to JSON file
                with open(filename_text, 'w', encoding='utf-8') as json_file:
                    json.dump(json_structure, json_file, indent=2)

                output_text_field.value = f"JSON saved to {filename_text}"

            save_json_shareGPT.click(on_save_button_click,[question_text_field,answer_text_field,output_filename,conversation_id_record])




User_Interface_GUI.launch()
