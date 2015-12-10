

import dts_calculate,mi

DELTA_1 = -2
DELTA_2 = -1
DELTA_3 = 0
KESI_1 = 0
KESI_2 = 1
KESI_3 = 2
THETA = 3.5

class judge:
    def __init__(self):
        self.dts_mean = 0
        self.dts_standard_derivation = 0
        self.dts_list = []
        self.mi_mean = 0
        self.mi_standard_derivation = 0
        self.mi_list = []
        self.mark_list = []
    def judge_local_max(self,num):
        if num == 0:
            return self.dts_list[num] > self.dts_list[num + 1]
        elif num == len( self.dts_list ) - 1:
            return self.dts_list[num] > self.dts_list[num - 1]
        else:
            return self.dts_list[num] > self.dts_list[num - 1] and self.dts_list[num] > self.dts_list[num + 1]

    def judge_local_min(self,num):
        if num == 0:
            return self.dts_list[num] < self.dts_list[num + 1]
        elif num == len( self.dts_list ) - 1:
            return self.dts_list[num] < self.dts_list[num - 1]
        else:
            return self.dts_list[num] < self.dts_list[num - 1] and self.dts_list[num] < self.dts_list[num + 1]

    def calculate_height_or_deepth_of_local_ext(self,num):
        if num == 0:
            ext_dts = self.dts_list[num] - self.dts_list[num + 1]
        elif num == len( self.dts_list ) - 1:
            ext_dts = self.dts_list[num] - self.dts_list[num - 1]
        else:
            ext_dts = min(self.dts_list[num] - self.dts_list[num - 1],self.dts_list[num] - self.dts_list[num + 1])
        return ext_dts

    def judge_right_second_local_max(self,num):  # "num" is the current number, i.e. the index of the potential second local maximum.
        if num != 0 and self.judge_local_max(num - 1):
            if num == 1:
                return self.dts_list[num] > self.dts_list[num + 1]
            elif num == len( self.dts_list ) - 1:
                return self.dts_list[num] > self.dts_list[num - 2]
            else:
                return self.dts_list[num] > self.dts_list[num - 2] and self.dts_list[num] > self.dts_list[num + 1]
        else:
            return False

    def judge_left_second_local_max(self,num):  # "num" is the current number, i.e. the index of the potential second local maximum.
        if num != ( len(self.dts_list) - 1 ) and self.judge_local_max(num + 1):
            if num == 0:
                return self.dts_list[num] > self.dts_list[num + 2]
            elif num == len( self.dts_list ) - 2:
                return self.dts_list[num] > self.dts_list[num - 1]
            else:
                return self.dts_list[num] > self.dts_list[num - 1] and self.dts_list[num] > self.dts_list[num + 2]
        else:
            return False

    def judge_right_second_local_min(self,num):  # "num" is the current number, i.e. the index of the potential second local minimum.
        if num != 0 and self.judge_local_min(num - 1):
            if num == 1:
                return self.dts_list[num] < self.dts_list[num + 1]
            elif num == len( self.dts_list ) - 1:
                return self.dts_list[num] < self.dts_list[num - 2]
            else:
                return self.dts_list[num] < self.dts_list[num - 2] and self.dts_list[num] < self.dts_list[num + 1]
        else:
            return False

    def judge_left_second_local_min(self,num):  # "num" is the current number, i.e. the index of the potential second local minimum.
        if num != ( len(self.dts_list) - 1 ) and self.judge_local_min(num + 1):
            if num == 0:
                return self.dts_list[num] < self.dts_list[num + 2]
            elif num == len( self.dts_list ) - 2:
                return self.dts_list[num] < self.dts_list[num - 1]
            else:
                return self.dts_list[num] < self.dts_list[num - 1] and self.dts_list[num] < self.dts_list[num + 2]
        else:
            return False

    def calculate_distance_right_local_ext(self,num):
        dis = abs( self.dts_list[num] - self.dts_list[num - 1] )
        return dis

    def calculate_distance_left_local_ext(self,num):
        dis = abs( self.dts_list[num] - self.dts_list[num + 1] )
        return dis

    def calculate_lrmin(self,num):
        if num == 0:
            lrmin = abs( self.dts_list[num] - self.dts_list[num + 2] )
        elif num == len( self.dts_list ) - 1 or num == len( self.dts_list ) - 2:
            lrmin = abs( self.dts_list[num] - self.dts_list[num - 1] )
        else:
            lrmin = min(abs( self.dts_list[num] - self.dts_list[num + 2] ) , abs( self.dts_list[num] - self.dts_list[num - 1] ))
        return lrmin

    def case_Ac_or_Cb(self,num):
        if self.judge_local_max(num):
            h_dts = self.calculate_height_or_deepth_of_local_ext(num)
            if h_dts > DELTA_1:
                return "bound"
            else:
                return "?"
        elif self.judge_local_min(num):
            d_dts = self.calculate_height_or_deepth_of_local_ext(num)
            if d_dts > KESI_2:
                return "separated"
            else:
                return "?"
        else:
            return "?"

    def case_Bc_or_Db(self,num):
        if self.judge_local_max(num):
            h_dts = self.calculate_height_or_deepth_of_local_ext(num)
            if h_dts > DELTA_2:
                return "bound"
            else:
                return "?"
        elif self.judge_local_min(num):
            d_dts = self.calculate_height_or_deepth_of_local_ext(num)
            if d_dts > KESI_1:
                return "separated"
            else:
                return "?"
        else:
            return "?"

    def case_Cc(self,num):
        if self.judge_local_max(num):
            h_dts = self.calculate_height_or_deepth_of_local_ext(num)
            if h_dts > DELTA_3:
                return "bound"
            else:
                return "?"
        elif self.judge_local_min(num):
            return "separated"
        else:
            return "?"

    def case_Bb(self,num):
        if self.judge_local_max(num):
            return "bound"
        elif self.judge_local_min(num):
            d_dts = self.calculate_height_or_deepth_of_local_ext(num)
            if d_dts > KESI_3:
                return "separated"
            else:
                return "?"
        else:
            return "?"

    def case_second_round(self,num):
        lrmin = self.calculate_lrmin(num)
        if self.judge_left_second_local_max(num) or self.judge_left_second_local_min(num):
            dis = self.calculate_distance_left_local_ext(num)
            if dis < 0.5 * lrmin:
                return "right"
            else:
                return "?"
        elif self.judge_right_second_local_max(num) or self.judge_right_second_local_min(num):
            dis = self.calculate_distance_right_local_ext(num)
            if dis < 0.5 * lrmin:
                return "left"
            else:
                return "?"
        else:
            return "?"

    def first_round(self):
        length = len(self.dts_list)
        self.mark_list = [0] * length
        for num in range(length):
            current_dts = self.dts_list[num]
            current_mi = self.mi_list[num]
            A = current_dts > self.dts_standard_derivation
            B = 0 < current_dts <= self.dts_standard_derivation
            C = -self.dts_standard_derivation < current_dts <= 0
            D = current_dts <= -self.dts_standard_derivation
            a = current_mi > self.mi_mean + self.mi_standard_derivation
            b = self.mi_mean < current_mi <= self.mi_mean + self.mi_standard_derivation
            c = self.mi_mean -self. mi_standard_derivation < current_mi <= self.mi_mean
            d = current_mi <= self.mi_mean - self.mi_standard_derivation
            if a or ( A and b ):  # Case: Aa or Ba or Ca or Da or Ab
                self.mark_list[num] = "bound"
            elif d or ( D and c ): # Case: Ad or Bd or Cd or Dd or Dc
                self.mark_list[num] = "separated"
            elif ( A and c ) or ( C and b ):  # Case: Ac or Cb
                self.mark_list[num] = self.case_Ac_or_Cb(num)
            elif ( B and c ) or ( D and b ):  # Case: Bc or Db
                self.mark_list[num] = self.case_Bc_or_Db(num)
            elif C and c:  # Case: Cc
                self.mark_list[num] = self.case_Cc(num)
            elif B and b:  # Case: Bb
                self.mark_list[num] = self.case_Bb(num)
            else:       # other cases
                self.mark_list[num] = "?"

    def second_round(self):
        length = len(self.dts_list)
        for num in range(length):
            if self.mark_list[num] == "?":
                self.mark_list[num] = self.case_second_round(num)

    def third_round(self):
        length = len(self.mark_list)
        for num in range(length):
            if self.mark_list[num] == "?":
                if self.mi_list[num] >= THETA:
                    self.mark_list[num] = "bound"
                else:
                    self.mark_list[num] = "separated"
            else:
                pass

    def main(self):
        self.first_round()
        self.second_round()
        self.third_round()
        return self.mark_list
