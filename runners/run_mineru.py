import os
import json
import time
from pathlib import Path
from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.config.enums import SupportedPdfParseMethod
from magic_pdf.data.read_api import read_local_office


input_path = "C:/Users/MattEvitts/parser_demo/gh_Examples/"  # path to input directory
output_path = "C:/Users/MattEvitts/parser_demo/outputs/mineru_results" # path to output directory

def parse_pdf(source, name, image_writer, json_writer, md_writer, image_dir):
    print(f"Processing {name} as PDF...")

    # set up readers for images and JSON
    reader = FileBasedDataReader("")
    pdf_bytes = reader.read(source)  # read the pdf content as loader takes bytes
    # load into format
    dataset = PymuDocDataset(pdf_bytes)

    if dataset.classify() == SupportedPdfParseMethod.OCR:
        print(f"Processing {name} with OCR...")
        # Perform OCR and document analysis
        doc_result = dataset.apply(doc_analyze, ocr=True).pipe_ocr_mode(image_writer)
    else:
        doc_result = dataset.apply(doc_analyze, ocr=False).pipe_txt_mode(image_writer)

    doc_result.dump_middle_json(json_writer, f"{name}.json")
    doc_result.dump_md(md_writer, f"{name}.md", image_dir)
    print(f"Saved JSON and MD for {name}")


def parse_office(source, name, image_writer, json_writer, md_writer, image_dir):

    file_type = source.split(".")[-1].lower()
    print(f"Processing {name} as {file_type}...")

    ds = read_local_office(source)[0]

    result = ds.apply(doc_analyze, ocr=True).pipe_txt_mode(image_writer)
    result.dump_middle_json(json_writer, f"{name}.json")
    result.dump_md(md_writer, f"{name}.md", image_dir)
    print(f"Saved JSON and MD for {name}")


def main():
    overall_start_time = time.time()
    print(f"Starting processing in {input_path}...")


    for file in os.listdir(input_path):
        start_time = time.time()
        source = os.path.join(input_path, file)
        name = Path(source).stem
        print(f"Converting {name} ...")

        # Define directories for images and JSON files
        local_image_dir, local_json_dir = os.path.join(output_path, "json_elements", "images"), os.path.join(output_path, "json_elements", "output")
        local_md_dir = os.path.join(output_path, "markdown")
        image_dir = str(os.path.basename(local_image_dir)) 

        # create directories if they do not exist
        os.makedirs(local_image_dir, exist_ok=True)
        os.makedirs(local_json_dir, exist_ok=True)
        os.makedirs(local_md_dir, exist_ok=True)

        # set up writers for images and JSON
        image_writer, json_writer, md_writer = FileBasedDataWriter(local_image_dir), FileBasedDataWriter(local_json_dir), FileBasedDataWriter(local_md_dir)

        #split here for pdf and docx files
        if file.lower().endswith(".pdf"):
            parse_pdf(source, name, image_writer, json_writer, md_writer, image_dir)

        #for office files
        else:
            parse_office(source, name, image_writer, json_writer, md_writer, image_dir)

        #write parse time to file
        end_time = time.time()
        elapsed_time = end_time - start_time
        with open(f"C:/Users/MattEvitts/parser_demo/outputs/mineru_results/mineru_parse_times.txt", "a") as time_file:
            time_file.write(f"{name}: {elapsed_time:.2f} seconds\n")

        print(f"Finished processing {name}. Time taken: {elapsed_time:.2f} seconds")

    # write overall time taken
    with open(f"C:/Users/MattEvitts/parser_demo/outputs/mineru_results/mineru_parse_times.txt", "a") as overall_file:
        overall_end_time = time.time()
        overall_elapsed_time = overall_end_time - overall_start_time
        overall_file.write(f"Total time taken: {overall_elapsed_time:.2f} seconds\n")

    print(f"All files processed. Total time taken: {overall_elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()

