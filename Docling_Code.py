import logging
import time
import sys
from pathlib import Path
from docling.backend.docling_parse_backend import DoclingParseDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    EasyOcrOptions,
    OcrMacOptions,
    PdfPipelineOptions,
    RapidOcrOptions,
    TesseractCliOcrOptions,
    TesseractOcrOptions,
)
from docling_core.types.doc import ImageRefMode, PictureItem, TableItem
from docling.document_converter import DocumentConverter, PdfFormatOption

# Constants
IMAGE_RESOLUTION_SCALE = 2.0

def main(input_doc_path):
    logging.basicConfig(level=logging.INFO)

    # Paths
    input_doc_path = Path(input_doc_path)
    output_dir = Path("scratch")

    # Pipeline options
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True
    pipeline_options.images_scale = IMAGE_RESOLUTION_SCALE
    pipeline_options.generate_page_images = True
    pipeline_options.generate_picture_images = True

    # OCR options (choose your preferred OCR engine here)
    ocr_options = TesseractCliOcrOptions(force_full_page_ocr=True)
    pipeline_options.ocr_options = ocr_options

    # Document converter setup
    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    # Conversion and processing
    start_time = time.time()
    conv_res = doc_converter.convert(input_doc_path)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_filename = conv_res.input.file.stem

    # Save page images
    total_pages = len(conv_res.document.pages)
    for page_no, page in conv_res.document.pages.items():
        page_image_filename = output_dir / f"{doc_filename}-{page_no}.png"
        with page_image_filename.open("wb") as fp:
            page.image.pil_image.save(fp, format="PNG")
        logging.info(f"Page {page_no}/{total_pages} processed.")

    # Save images of figures and tables
    table_counter = 0
    picture_counter = 0
    for element, _level in conv_res.document.iterate_items():
        if isinstance(element, TableItem):
            table_counter += 1
            element_image_filename = (
                output_dir / f"{doc_filename}-table-{table_counter}.png"
            )
            with element_image_filename.open("wb") as fp:
                element.get_image(conv_res.document).save(fp, "PNG")
            logging.info(f"Table {table_counter} processed.")

        if isinstance(element, PictureItem):
            picture_counter += 1
            element_image_filename = (
                output_dir / f"{doc_filename}-picture-{picture_counter}.png"
            )
            with element_image_filename.open("wb") as fp:
                element.get_image(conv_res.document).save(fp, "PNG")
            logging.info(f"Picture {picture_counter} processed.")

    # Save Markdown with embedded pictures
    md_embedded_filename = output_dir / f"{doc_filename}-with-images.md"
    conv_res.document.save_as_markdown(md_embedded_filename, image_mode=ImageRefMode.EMBEDDED)
    logging.info("Markdown with embedded pictures saved.")

    # Save Markdown with externally referenced pictures
    md_referenced_filename = output_dir / f"{doc_filename}-with-image-refs.md"
    conv_res.document.save_as_markdown(md_referenced_filename, image_mode=ImageRefMode.REFERENCED)
    logging.info("Markdown with image references saved.")

    # Create a specific directory for plain markdown file inside scratch
    md_output_dir = output_dir / f"{doc_filename}-md"
    md_output_dir.mkdir(parents=True, exist_ok=True)

    # Export plain Markdown from document in the separate directory
    plain_md = conv_res.document.export_to_markdown()
    plain_md_filename = md_output_dir / f"{doc_filename}-plain.md"
    with plain_md_filename.open("w") as fp:
        fp.write(plain_md)

    # Logging completion
    end_time = time.time() - start_time
    logging.info(f"Document converted and figures exported in {end_time:.2f} seconds.")
    logging.info(f"Plain Markdown file saved at: {plain_md_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python docling_script.py <path_to_pdf>")
        sys.exit(1)
    main(sys.argv[1])
