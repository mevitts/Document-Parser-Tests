# Document Parser Performance Comparison: Docling vs. MinerU

This project contains two Python scripts designed to compare the overall speed and quality of two document parsing libraries: **Docling** and **MinerU**.
Along with converting various document types (PDF, DOCX, PPTX) into standardized formats (JSON and Markdown), the scripts also log the processing time for each file, allowing for a direct performance benchmark.
This evaluation task was built during an internship following extensive research looking at selecting the optimal document intelligence tool based on speed and parsing accuracy.

---

## Key Features

* **Multi-Format Support**: Parses PDF, DOCX, PPTX, and XLSX files.
* **Dual Library Evaluation**: Contains separate, self-contained scripts for testing `docling` and `mineru`.
* **Dual Output Format**: Saves the parsed document structure as both a detailed **JSON** file and a human-readable **Markdown** file.
* **Performance Benchmarking**: Records the time taken to process each individual file and calculates the total time for the entire batch.
* **OCR Integration**: Automatically handles both text-based and scanned (image-based) documents requiring Optical Character Recognition (OCR).

---

## How It Works

The evaluation is split into two scripts, one for each library. Both scripts read files from a common input directory but write their results to separate output directories to keep the evaluation clean.

### 1. Docling Parser Script

This script utilizes the `docling` library to perform document conversion.

**Initialization and Processing**
* The script first downloads the necessary `RapidOCR` models from Hugging Face Hub. These models are used for detecting and recognizing text in scanned documents.
* It then configures `PdfPipelineOptions` to enable layout analysis, table extraction (`TableFormerMode.ACCURATE`), and OCR capabilities using the downloaded models.
* A central `DocumentConverter` is initialized with these settings, configured to handle PDF, DOCX, PPTX, and XLSX files.
* Iterating through the files, each document is parsed and dumped as **JSON** and **Markdown** files.
* The time taken for the entire process is recorded in `docling_parse_times.txt`.

### 2. Mineru Parser Script

This script uses the `magic_pdf` library, which has different workflows for PDF and other Office files.

**Initialization and Processing**
* First sets up `FileBasedDataWriter` objects to manage the output of JSON files, Markdown files, and any extracted images.

* **For PDF Files:**
    1.  The PDF is loaded into a `PymuDocDataset`.
    2.  The script calls `dataset.classify()` to determine if the PDF is text-based or requires OCR.
    3.  Final result is dumped to **JSON** and **Markdown** files.

* **For Office Files (`.docx`, `.pptx`, etc.):**
    1.  Files are loaded using the `read_local_office` function.
    2.  The loaded object is then processed through the `doc_analyze` pipeline.
    3.  The result is similarly dumped to **JSON** and **Markdown** files.

The time taken for the entire process is recorded in `docling_parse_times.txt`.

---

## Usage Instructions

Follow these steps to run the evaluation:

**1. Install Dependencies:**
You will need to install the required Python libraries. It's recommended to do this in a virtual environment. The key libraries are `docling-core`, `magic-pdf-toolbox`, `huggingface-hub`, and their dependencies (like `pypdfium2` and `onnxruntime`).

**2. Configure Paths:**
Before running, you **must** update the following path variables at the top of both scripts to match your local machine's directory structure:

* `input_path`: The folder where your sample PDF, DOCX, and other files are located.
    * *Example: `"C:/Users/YourUser/Documents/parser_inputs/"`*
* `output_path`: The parent folder where the results will be saved. Each script will create its own subdirectory within this path (`docling_results` and `mineru_results`).
    * *Example: `"C:/Users/YourUser/Documents/parser_outputs/"`*

**3. Place Input Files:**
Add the documents you want to test into the folder you specified in the `input_path`.

**4. Run the Scripts:**
Execute each script from your terminal. They must be run separately.

```bash
# Run the Docling evaluation
python docling_parser_script.py

# Run the Mineru evaluation
python mineru_parser_script.py
```

**Notes about performance:** These scripts were initially written and tested for CPU usage, however both Docling and MinerU have much higher performance with GPU capabilities. 
