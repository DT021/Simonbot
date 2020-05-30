import UsefullMessageManipulationFunctions as Umm
import os

file_to_write_to = open("Conversations.txt", "w")
nr_lines_in_block = 0

src_folder = "C:/Users/sular/Desktop/inbox"
# loop through the subfolders
for root, folders, filenames in os.walk(src_folder, topdown=False):
    for file in sorted(filenames):
        file_path = os.path.join(root, file)
        something_written = False
        if "message_" in file:
            print(file_path)
            for message in zip(Umm.return_messages_from_json_file(file_path)[0],
                               Umm.return_messages_from_json_file(file_path)[1]):
                print(message)
                if nr_lines_in_block <= 14:   # how many lines a conversation block should have
                    try:
                        file_to_write_to.write(message[1])
                        file_to_write_to.write("\n")
                        nr_lines_in_block += 1
                    except UnicodeEncodeError:  # If I get a unicode error just skip that line
                        continue
                else:
                    try:
                        file_to_write_to.write(message[1])
                        file_to_write_to.write("\n\n\n")
                        nr_lines_in_block = 0
                    except UnicodeEncodeError:
                        continue
file_to_write_to.close()
