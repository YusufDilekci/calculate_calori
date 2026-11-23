import gradio as gr
from calculate_calori.models import generate_image

with gr.Blocks() as demo:
    gr.Markdown("## Yemek Fotoğrafı Yükle")
    with gr.Row():
        image = gr.Image(label="Yemek Fotoğrafı", type="filepath", height=300)
        with gr.Column():
            textbox = gr.Textbox(label="Yemek Açıklaması (isteğe bağlı)")
            button = gr.Button("Kaloriyi Hesapla")
            output = gr.Markdown(label="Sonuç")
    button.click(fn=generate_image, inputs=[image, textbox], outputs=output)

demo.launch(share=True)