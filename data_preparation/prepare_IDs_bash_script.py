def main():

    # file to save the processed data from data-all-docs.json
    output_file = open("preprocessed_IDs_bash_script.json", "w")

    # count number of doc ids
    count = 0

    with open("all_EMA_document_IDs_type_product_information.json") as file:
        file_content = file.readlines()

        for line in file_content:
            count += 1

            # pre-process doc ids by removing "" and ,
            line = line.replace('"', '')
            line = line.replace(',', '')

            # write to a file
            output_file.write(line)

    output_file.close()

    print("Total number of doc ids: {}".format(count))


if __name__ == '__main__':
    main()