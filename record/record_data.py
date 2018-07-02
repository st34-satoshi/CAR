# save and read the record.
from player import cop
from player import robber
from environment import make_environment


class Record:
    # the list of every data.it contains the scene.
    # 全てを順番に保存する。stringで保存,(cops_number,cops,robber_number,robber)の場面毎のリスト
    record_all = []
    # the data read.the list of the pair of the cops and robbers.
    # 読み込んだデータcops,robberのリストのペアの配列
    record_read = []
    count = 0  # when this is 1, save the scene.カウントが1の時にその場面を保存する
    count_cycle = 2  # the period to save the scene.どのくらいの周期で保存するか
    max_amount_save = 10000

    def __init__(self):
        self.record_all = []
        self.record_read = []
        self.count = 0

    def add_data(self, record_data):
        # combine record_data
        for record in record_data.record_all:
            self.record_all.append(record)
        for record in record_data.record_read:
            self.record_read.append(record)

    def reset_all(self):
        # reset the variables
        self.record_all = []
        self.record_read = []
        self.count = 0

    def get_scene_at(self, number_scene):
        # return the cops and robbers list at the scene of the scene number.
        # if the scene number is strange return the present scene.
        # number_sceneの場面のプレイヤーのリストを返す。number_sceneがおかしければ今の状態を返す
        max_len = len(self.record_read)
        if number_scene < 0:
            return 0, self.record_read[0][0], self.record_read[0][1]
        if number_scene >= max_len:
            return max_len-1, self.record_read[max_len-1][0], self.record_read[max_len-1][1]
        return number_scene, self.record_read[number_scene][0], self.record_read[number_scene][1]

    def __save(self, list_cops, list_robbers):
        # get the cops and robbers list , changing to the string , then save it.
        # それぞれのリストを受け取ってストリングにして保存する
        list_cops_robbers = [str(len(list_cops))]  # first is how many.copとrobberのリストそれぞれ何体いるかも保存する,最初はcop何体いるか
        for cp in list_cops:
            list_cops_robbers.append(cp.get_record_string())
        list_cops_robbers.append(str(len(list_robbers)))
        for rob in list_robbers:
            # start to save robbers data.robberの情報を保存して行く
            list_cops_robbers.append(rob.get_record_string())
        self.record_all.append(list_cops_robbers)

    def save_to_filename_file_all(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(len(self.record_all)) + "\n")
            for list_cr in self.record_all:
                for st in list_cr:
                    f.write(st + "\n")
        print('saved all to ' + filename)

    def save_to_file_one(self, number_scene):
        # save one scene to the file.
        # 一つの場面だけを記録,ファイルを読み込んでいる時にやる
        if 0 <= number_scene < len(self.record_read):
            self.record_all = []
            cp = self.record_read[number_scene]
            self.__save(cp[0], cp[1])
            with open("record/CAR-record-one.txt", "w", encoding="utf-8") as f:
                f.write(str(len(self.record_all)) + "\n")
                for list_cr in self.record_all:
                    for st in list_cr:
                        f.write(st + "\n")
            print('saved one to record/CAR-record-one.txt')

    def save_record_from_read(self, filename):
        # save record from record_read
        self.record_all = []
        for scene in range(len(self.record_read)):
            self.__save(self.record_read[scene][0], self.record_read[scene][1])
        self.save_to_filename_file_all(filename)

    def read_from_file(self, file_name):
        # read the saved file. this method can be used when both all record read and one scene read.
        # 全体の動きを読み込む時も、一つの場面だけを読み込む時も使える
        self.record_read = []
        with open(file_name, "r") as f:
            data = f.readlines()  # the array of line by line.行毎の配列
            # delete the read data from the head.読み込んだデータを先頭から消して行く
            count_times = int(data.pop(0))  # first is the number how many scene is saved.何回分のデータが保存されているか
            for time in range(count_times):
                list_cops = []
                number_cops = int(data.pop(0))  # the number how many cops are.copsが何体いるか
                for i in range(number_cops):
                    cp = cop.Cop(environment=make_environment.make_environment(), id=0)
                    cp.read_from_data(data)
                    list_cops.append(cp)
                list_robbers = []
                number_robbers = int(data.pop(0))
                for i in range(number_robbers):
                    rob = robber.Robber(environment=make_environment.make_environment(), id=0)
                    rob.read_from_data(data)
                    list_robbers.append(rob)
                self.record_read.append((list_cops, list_robbers))
        print('read : ' + file_name)

    def save_record(self, list_cops, list_robbers):
        # if the count is 0 , save this scene.countが0なら保存する
        # if data is over the max amount of saving.  no to save
        if self.max_amount_save == len(self.record_all):
            print("over the max amout of saving date!")
        if self.max_amount_save >= len(self.record_all):
            if self.count == 0:
                self.__save(list_cops, list_robbers)
            self.count += 1
            if self.count > self.count_cycle:
                self.count = 0

