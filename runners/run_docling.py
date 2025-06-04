import os
from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableFormerMode,
    RapidOcrOptions,
)
from docling.document_converter import (
    ConversionResult,
    DocumentConverter,
    InputFormat,
    PdfFormatOption,
)
from huggingface_hub import snapshot_download

#artifacts_path = "C:/Users/MattEvitts/.cache/docling/models"

input_path = "C:/Users/MattEvitts/parser_demo/ExampleDocuments/"  # path to input directory
output_path = "C:/Users/MattEvitts/parser_demo/outputs/docling_results" # path to output directory
download_path = snapshot_download(repo_id="SWHL/RapidOCR", cache_dir="C:/Users/MattEvitts/.cache/huggingface/hub", local_files_only=False)

def main():

    for file in os.listdir(input_path):
        if file.endswith(".pdf"):
            source = os.path.join(input_path, file)
            name = Path(source).name
            print(f"Converting {name} to markdown...")
            convert_pdf_to_markdown(source, name)
        else:
            print(f"Skipping {file}, not a PDF file.")

def convert_pdf_to_markdown(source, name):
    print(f"Converting {name} to markdown...")

    #download RapidOCR weights
    print("Downloading RapidOCR models")

    # Setup RapidOcrOptions for english detection
    det_model_path = os.path.join(
        download_path, "PP-OCRv4", "en_PP-OCRv3_det_infer.onnx"
    )
    rec_model_path = os.path.join(
        download_path, "PP-OCRv4", "ch_PP-OCRv4_rec_server_infer.onnx"
    )
    cls_model_path = os.path.join(
        download_path, "PP-OCRv3", "ch_ppocr_mobile_v2.0_cls_train.onnx"
    )

    ocr_options = RapidOcrOptions(
        det_model_path=det_model_path,
        rec_model_path=rec_model_path,
        cls_model_path=cls_model_path,
    )

    # Setup PdfPipelineOptions with OCR and table extraction
    pipeline_options = PdfPipelineOptions(
        ocr_options=ocr_options,
        do_layout_analysis=True,
        do_table_extraction=True
    )
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
    pipeline_options.table_structure_options.do_cell_matching = False

    #limit for now on 70 pages
    # Convert the document
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            ),
        },
    )

    print("Converting")
    conversion_result: ConversionResult = converter.convert(source=source)
    doc = conversion_result.document

    print("Markdown conversion:")
    md = doc.export_to_markdown()
    print(md)

    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f"{name}.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    main()
