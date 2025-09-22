import os
if __name__ == "__main__":

    filename = os.path.join(os.getcwd(), "Data", "app_log (logfil analyse) - random.txt")

    dict_of_messages = {} # messages are stored by type as a dict of lists

    with open(filename) as f: #open file
        lines = f.readlines()
    for line in lines:

        message = line.strip()
        words = message.split()
        # the type is after two spaces
        if words[2] not in dict_of_messages: #if this type of message is not initialized in the dict, make a new one
            dict_of_messages[words[2]] = []
        dict_of_messages[words[2]].append(message) #append message to list
    for key in dict_of_messages: # for each error type
        out_path = os.path.join("Logfile_Analysis", "Output", f"{key}.txt") #wrte at new file named after the type
        with open(out_path, "w", encoding="utf-8") as out:
            for message in dict_of_messages[key]:
                out.write("".join(message) + ("\n" if message else "")) #write each element in the list to it