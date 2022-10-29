


class WeirdJson:
    # initialise by reading file contents
    def __init__(self, json_file):
        self.json_file = json_file
        with open(json_file) as f:
            for line in f:
                print(line)



if __name__ == '__main__':
    wj = WeirdJson('keyboard-layout_1.json')