import os
import zipfile

def unzip_specific_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".zip"):
                output_folder = directory + file.split("_")[0]
                try:
                    os.mkdir(output_folder)
                except Exception:
                    print(1)
                zip_file_path = os.path.join(root, file)
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    for file_info in zip_ref.infolist():
                        if file_info.filename.__contains__("OG/html") and file_info.filename.endswith("html"):
                            filename = os.path.basename(file_info.filename)
                            extracted_path = os.path.join(output_folder, filename)
                            with open(extracted_path, 'wb') as extracted_file:
                                extracted_file.write(zip_ref.read(file_info.filename))
                print(f"{file} unzipped successfully.")

for yrs in range(2024, 2025):
    if __name__ == "__main__":
        directory = "./patentZip/" + str(yrs) + "/"
        unzip_specific_files(directory)
