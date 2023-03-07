

class FileCorrector:
    def __init__(self, file_path = "logs.txt", new_file_path = "logs_new.txt"):
        self.file_path = file_path
        self.new_file_path = new_file_path

    def correct(self):
        with open(self.file_path) as fin:
            new_lines = ""
            input_lines = fin.readlines()
            for line in input_lines[2:]:
                line = line.replace("\n", ";\n")
                commands = line.split(";")
                if len(commands) < 15:
                    continue
                time_command_pointer = commands.index("SAVED_TIME")
                time = commands[time_command_pointer + 1][11:]
                date = commands[time_command_pointer + 1][:10]
                commands[time_command_pointer + 1] = f"{time}"
                commands.insert(time_command_pointer, f"{date}")
                commands.insert(time_command_pointer, f"SAVED_DATE")
                new_lines += ";".join(commands)
                new_lines = new_lines.replace(";;", ";")
            fin.close()

        with open(self.new_file_path, "w") as fout:
            fout.write(new_lines)
            fout.close()



        with open("tags.txt") as f:
            
            final_lines = ""
            lines = f.readlines()
            ID = 1
            for line in lines:
                l = f.readline()
                l = line.split(";")
                print(l)
                final_lines += f"EMPLOYEE_ID;{ID};TAG;{l[0]};Jmeno;{l[1]};Prijmeni;{l[2]};Song;{l[3]};Permissions;NONE;".replace("\n", "")+"\n"
                ID += 1
            f.close()

            with open("tags_new.txt", "w") as fout2:
                fout2.write(final_lines[:-1])

if __name__ == "__main__":
    file_corrector = FileCorrector()
    file_corrector.correct()