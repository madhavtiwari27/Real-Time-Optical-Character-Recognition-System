import argparse
import os
import OCR
import LIG
import pytesseract
import subprocess

def main():
    
    parser = argparse.ArgumentParser(description="Real-time OCR script")

    requiredNamed = parser.add_argument_group('required named arguments')

    requiredNamed.add_argument('-t', '--tess_path',
                               help="path to the cmd root of tesseract install",
                               metavar='', required=True)

    parser.add_argument('-c', '--crop', help="crop OCR area in pixels (two vals required): width height",
                        nargs=2, type=int, metavar='')

    parser.add_argument('-v', '--view_mode', help="view mode for OCR boxes display (default=1)",
                        default=1, type=int, metavar='')
    parser.add_argument('-sv', '--show_views', help="show the available view modes and descriptions",
                        action="store_true")

    parser.add_argument("-l", "--language",
                        help="code for tesseract language, use + to add multiple (ex: chi_sim+chi_tra)",
                        metavar='', default=None)
    parser.add_argument("-sl", "--show_langs", help="show list of tesseract (4.0+) supported langs",
                        action="store_true")
    parser.add_argument("-s", "--src", help="SRC video source for video capture",
                        default=0, type=int)

    args = parser.parse_args()

    print("Parsed arguments:", args)

    tess_path = os.path.normpath(args.tess_path)
    print("Normalized tess_path:", tess_path)

    pytesseract.pytesseract.tesseract_cmd = tess_path

    if not os.path.isfile(tess_path):
        print(f"Error: The specified Tesseract path does not exist: {tess_path}")
        return

    try:
        tesseract_version = subprocess.check_output([tess_path, '--version'])
        print("Tesseract version:", tesseract_version.decode().strip())
    except subprocess.CalledProcessError as e:
        print(f"Error: Tesseract executable at {tess_path} cannot be run. Error: {e}")
        return
    except FileNotFoundError:
        print(f"Error: Tesseract executable not found at {tess_path}.")
        return

    if args.show_langs:
        LIG.show_codes()
        return

    if args.show_views:
        print(OCR.views.__doc__)
        return

    OCR.tesseract_location(tess_path)
    OCR.ocr_stream(view_mode=args.view_mode, source=args.src, crop=args.crop, language=args.language)


if __name__ == '__main__':
    main()
    
