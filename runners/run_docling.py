import os
import json
import time
from pathlib import Path
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat

from docling.pipeline.vlm_pipeline import VlmPipeline
from docling.datamodel.pipeline_options_vlm_model import ApiVlmOptions, ResponseFormat
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
    ExcelFormatOption,
    WordFormatOption,
    PowerpointFormatOption,
)
from huggingface_hub import snapshot_download

input_path = "C:/Users/MattEvitts/parser_demo/gh_Examples/"  # path to input directory
output_path = "C:/Users/MattEvitts/parser_demo/outputs/docling_results" # path to output directory

download_path = snapshot_download(repo_id="SWHL/RapidOCR", cache_dir="C:/Users/MattEvitts/.cache/huggingface/hub", local_files_only=False)

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

#standard converted 
converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
            InputFormat.DOCX: WordFormatOption(pipeline_options=pipeline_options),
            InputFormat.PPTX: PowerpointFormatOption(pipeline_options=pipeline_options),
            InputFormat.XLSX: ExcelFormatOption(pipeline_options=pipeline_options),
        },
    )

def convert_and_save(source, output_dir, name):
    try:
        result: ConversionResult = converter.convert(source=source)
        doc_dict = result.document.export_to_dict()

        #convert to json
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "json", f"{name}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(doc_dict, f, indent=2, ensure_ascii=False)
        

        #convert to markdown
        doc = result.document
        md = doc.export_to_markdown()

        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "markdown", f"{name}.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"Saved: {output_file}")

    except Exception as e:
        print(f"Error processing {name}: {e}")

def main():
    overall_start_time = time.time()

    for file in os.listdir(input_path):
        start_time = time.time()
        end = file.lower()
        if not end.endswith((".pdf", ".docx", ".pptx", ".xlsx")):
            continue
        source = os.path.join(input_path, file)
        name = Path(source).name
        print(f"Converting {name} to json and md...")
        await convert_and_save(source, output_path, name)

        #write parse time to file
        end_time = time.time()
        elapsed_time = end_time - start_time
        with open(f"C:/Users/MattEvitts/parser_demo/outputs/docling_results/docling_parse_times.txt", "a") as time_file:
            time_file.write(f"{name}: {elapsed_time:.2f} seconds\n")

        print(f"Finished processing {name}. Time taken: {elapsed_time:.2f} seconds")

    with open(f"C:/Users/MattEvitts/parser_demo/outputs/docling_results/docling_parse_times.txt", "a") as overall_file:
        overall_end_time = time.time()
        overall_elapsed_time = overall_end_time - overall_start_time
        overall_file.write(f"Total time taken: {overall_elapsed_time:.2f} seconds\n")

    print(f"All files processed. Total time taken: {overall_elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
