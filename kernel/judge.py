
"""
DELTA_1, DELTA_2, DELTA_3 are the "bound" condition parameter, which have the relationship of D1 < D2 < D3.
KESI_1, KESI_2, KESI_3 are the "separated" condition parameter, which have the relationship of K1 < K2 < K3.
THETA is the mi valve parameter, when the word's mi is above THETA, it tends to be bound and vice versa.
"""

DELTA_1 = 6
DELTA_2 = 8
DELTA_3 = 10
KESI_1 = 24
KESI_2 = 27
KESI_3 = 30
THETA = 3


class Judge:

    def __init__(self):
        """
        There are seven class properties.

        "dts_mean" represents the mean value of dtscore list.
        "dts_standard_derivation" represents the standard derivation of dtscore
        list.
        "dts_list" represents the dtscore list (only with numbers).
        "mi_mean" represents the mean value of mi list.
        "mi_standard_derivation" represents the standard derivation of mi list.
        "mi_list" represents the mi list (only with numbers).
        "mark_list" represents the mark list which has the relationships between
        all of the adjacent characters.
        """
        self.dts_mean = 0
        self.dts_standard_derivation = 0
        self.dts_list = []
        # Only setting the dts_list with only numbers in judge.py.

        self.mi_mean = 0
        self.mi_standard_derivation = 0
        mi_list = []
        # Only setting the mi_list with only numbers to judge.py.
        self.mi_list = mi_list[1:-1]
        # The first and the last element in mi_list contains the blank,
        # so it is of no use and should be abandoned.

        self.mark_list = []

    def judge_local_max(self, ind):
        """
        Judge whether the particular dtscore is the local maximum in the dtscore
         list.
        """
        if ind == 0:
            # If the particular dtscore's index is 0, only compare with its
            # right neighbor.
            return self.dts_list[ind] > self.dts_list[ind + 1]
        elif ind == len(self.dts_list) - 1:
            # If the particular dtscore is the last one in the list, only
            # compare with its left neighbor.
            return self.dts_list[ind] > self.dts_list[ind - 1]
        else:
            # In other cases, compare with its right neighbor and left neighbor.
            return self.dts_list[ind] > self.dts_list[ind - 1] and self.dts_list[ind] > self.dts_list[ind + 1]

    def judge_local_min(self, ind):
        """
        Judge whether the particular dtscore is the local minimum in the dtscore
        list.
        """
        if ind == 0:
            # If the particular dtscore's index is 0, only compare with its
            # right neighbor.
            return self.dts_list[ind] < self.dts_list[ind + 1]
        elif ind == len( self.dts_list ) - 1:
            # If the particular dtscore is the last one in the list, only
            # compare with its left neighbor.
            return self.dts_list[ind] < self.dts_list[ind - 1]
        else:
            # In other cases, compare with its right neighbor and left neighbor.
            return self.dts_list[ind] < self.dts_list[ind - 1] and self.dts_list[ind] < self.dts_list[ind + 1]

    def calculate_height_or_depth_of_local_ext(self, ind):
        """
        If the particular dtscore is the local extremum, then calculate the
        height of depth of it.
        The formula is:
            height_or_depth = min ( local_ext - value(left_neighbor),
                                    local_ext - value(right_neighbor) )
        """
        if ind == 0:
            # If the particular dtscore's index is 0, only compare with its
            # right neighbor.
            ext_dts = self.dts_list[ind] - self.dts_list[ind + 1]
        elif ind == len( self.dts_list ) - 1:
            # If the particular dtscore is the last one in the list, only
            # compare with its left neighbor.
            ext_dts = self.dts_list[ind] - self.dts_list[ind - 1]
        else:
            # In other cases, compare with its right neighbor and left neighbor.
            ext_dts = min( abs( self.dts_list[ind] - self.dts_list[ind - 1] ) ,
                           abs( self.dts_list[ind] - self.dts_list[ind + 1]) )
        return ext_dts

    def judge_right_second_local_max(self, ind):
        """
        This function will judge whether a certain element is the right second
        local maximum.

        "ind" is the index of the potential second local maximum.
        """
        if ind != 0 and self.judge_local_max(ind - 1):
            if ind == 1:
                # If the particular dtscore's index is 1, only compare with its
                # right neighbor.
                return self.dts_list[ind] > self.dts_list[ind + 1]
            elif ind == len(self.dts_list) - 1:
                # If the particular dtscore is the last one in the list, only
                # compare with its second left neighbor.
                return self.dts_list[ind] > self.dts_list[ind - 2]
            else:
                # In other cases, compare with its right neighbor and its second
                # left neighbor.
                return self.dts_list[ind] > self.dts_list[ind - 2] and self.dts_list[ind] > self.dts_list[ind + 1]
        else:
            return False

    def judge_left_second_local_max(self, ind):
        """
        This function will judge whether a certain element is the left second
        local maximum.

        "ind" is the index of the potential second local maximum.
        """
        if ind != ( len(self.dts_list) - 1 ) and self.judge_local_max(ind + 1):
            if ind == 0:
                # If the particular dtscore's index is 0, only compare with its
                # second right neighbor.
                return self.dts_list[ind] > self.dts_list[ind + 2]
            elif ind == len( self.dts_list ) - 2:
                # If the particular dtscore is the second last one in the list,
                # only compare with its left neighbor.
                return self.dts_list[ind] > self.dts_list[ind - 1]
            else:
                # In other cases, compare with its second right neighbor and its
                # left neighbor.
                return self.dts_list[ind] > self.dts_list[ind - 1] and self.dts_list[ind] > self.dts_list[ind + 2]
        else:
            return False

    def judge_right_second_local_min(self, ind):
        """
        This function will judge whether a certain element is the right second
        local minimum.

        "ind" is the index of the potential second local minimum.
        """
        if ind != 0 and self.judge_local_min(ind - 1):
            if ind == 1:
                # If the particular dtscore's index is 1, only compare with its
                # right neighbor.
                return self.dts_list[ind] < self.dts_list[ind + 1]
            elif ind == len(self.dts_list) - 1:
                # If the particular dtscore is the last one in the list, only
                # compare with its second left neighbor.
                return self.dts_list[ind] < self.dts_list[ind - 2]
            else:
                # In other cases, compare with its right neighbor and its second
                # left neighbor.
                return self.dts_list[ind] < self.dts_list[ind - 2] and self.dts_list[ind] < self.dts_list[ind + 1]
        else:
            return False

    def judge_left_second_local_min(self, ind):
        """
        This function will judge whether a certain element is the left second
        local minimum.

        "ind" is the index of the potential second local minimum.
        """
        if ind != (len(self.dts_list) - 1) and self.judge_local_min(ind + 1):
            if ind == 0:
                # If the particular dtscore's index is 0, only compare with its
                # second right neighbor.
                return self.dts_list[ind] < self.dts_list[ind + 2]
            elif ind == len(self.dts_list) - 2:
                # If the particular dtscore is the second last one in the list,
                # only compare with its left neighbor.
                return self.dts_list[ind] < self.dts_list[ind - 1]
            else:
                # In other cases, compare with its second right neighbor and its
                # left neighbor.
                return self.dts_list[ind] < self.dts_list[ind - 1] and self.dts_list[ind] < self.dts_list[ind + 2]
        else:
            return False

    def calculate_distance_right_local_ext(self, ind):
        """
        This function will calculate the distance between right second local
        extremum and its local extremum on the left side.
        The formula is:
            distance = abs ( right_second_local_extremum - value(left_neighbor) )

        "ind" is the index of the right second local extremum.
        """
        dis = abs( self.dts_list[ind] - self.dts_list[ind - 1] )
        return dis

    def calculate_distance_left_local_ext(self, ind):
        """
        This function will calculate the distance between left second local
        extremum and its local extremum on the right side.
        The formula is:
            distance = abs ( left_second_local_extremum - value(right_neighbor) )

        "ind" is the index of the left second local extremum.
        """
        dis = abs( self.dts_list[ind] - self.dts_list[ind + 1] )
        return dis

    def calculate_left_lrmin(self, ind):
        """
        This function will calculate the "lrmin" value of the left second local
        extremum, and that is, the minimum of the difference between its left
        neighbor and its second right neighbor.
        The formula is:
            distance = min( abs ( left_second_local_extremum - value(left_neighbor) ),
                            abs ( left_second_local_extremum - value(second_right_neighbor) ) )

        "ind" is the index of the left second local extremum.
        """
        if ind == 0:
            # If the particular dtscore's index is 0, only consider its
            # second right neighbor in calculation.
            lrmin = abs( self.dts_list[ind] - self.dts_list[ind + 2] )
        elif ind == len( self.dts_list ) - 1 or ind == len( self.dts_list ) - 2:
            # If the particular dtscore is the last one or the second last one
            # in the list, only consider its left neighbor in calculation.
            lrmin = abs( self.dts_list[ind] - self.dts_list[ind - 1] )
        else:
            lrmin = min(abs( self.dts_list[ind] - self.dts_list[ind + 2] ) ,
                        abs( self.dts_list[ind] - self.dts_list[ind - 1] ))
        return lrmin

    def calculate_right_lrmin(self, ind):
        """
        This function will calculate the "lrmin" value of the right second local
        extremum, and that is, the minimum of the difference between its right
        neighbor and its second left neighbor.
        The formula is:
            distance = min( abs ( right_second_local_extremum - value(right_neighbor) ),
                            abs ( right_second_local_extremum - value(second_left_neighbor) ) )

        "ind" is the index of the right second local extremum.
        """
        if ind == 0 or ind == 1:
            # If the particular dtscore's index is 0 or 1, only consider its
            # right neighbor in calculation.
            lrmin = abs( self.dts_list[ind] - self.dts_list[ind + 1] )
        elif ind == len( self.dts_list ) - 1:
            # If the particular dtscore is the last one in the list, only
            # consider its second left neighbor in calculation.
            lrmin = abs( self.dts_list[ind] - self.dts_list[ind - 2] )
        else:
            lrmin = min(abs( self.dts_list[ind] - self.dts_list[ind + 1] ) ,
                        abs( self.dts_list[ind] - self.dts_list[ind - 2] ))
        return lrmin

    def case_Ac_or_Cb(self, ind):
        """
        This is the case Ac and Cb.

        If the current element is the local maximum, compare its height with DELTA_1.
        If the current element is the local minimum, compare its depth with KESI_2.
        """
        if self.judge_local_max(ind):
            h_dts = self.calculate_height_or_depth_of_local_ext(ind)
            if h_dts > DELTA_1:
                return "bound1"
            else:
                return "?"
        elif self.judge_local_min(ind):
            d_dts = self.calculate_height_or_depth_of_local_ext(ind)
            if d_dts > KESI_2:
                return "separated2"
            else:
                return "?"
        else:
            return "?"

    def case_Bc_or_Db(self, ind):
        """
        This is the case Bc and Db.

        If the current element is the local maximum, compare its height with DELTA_2.
        If the current element is the local minimum, compare its depth with KESI_1.
        """
        if self.judge_local_max(ind):
            h_dts = self.calculate_height_or_depth_of_local_ext(ind)
            if h_dts > DELTA_2:
                return "bound2"
            else:
                return "?"
        elif self.judge_local_min(ind):
            d_dts = self.calculate_height_or_depth_of_local_ext(ind)
            if d_dts > KESI_1:
                return "separated1"
            else:
                return "?"
        else:
            return "?"

    def case_Cc(self, ind):
        """
        This is the case Cc.

        If the current element is the local maximum, compare its height with DELTA_3.
        If the current element is the local minimum, it means "separated".
        """
        if self.judge_local_max(ind):
            h_dts = self.calculate_height_or_depth_of_local_ext(ind)
            if h_dts > DELTA_3:
                return "bound3"
            else:
                return "?"
        elif self.judge_local_min(ind):
            return "separated"
        else:
            return "?"

    def case_Bb(self, ind):
        """
        This is the case Bb.

        If the current element is the local maximum, it means "bound".
        If the current element is the local minimum, compare its depth with KESI_3.
        """
        if self.judge_local_max(ind):
            return "bound"
        elif self.judge_local_min(ind):
            d_dts = self.calculate_height_or_depth_of_local_ext(ind)
            if d_dts > KESI_3:
                return "separated3"
            else:
                return "?"
        else:
            return "?"

    def case_second_round(self, ind):
        """
        This is the case of the second round.

        If the current element is the second local extremum, compare its
        distance with its lrmin value.
        """
        if (self.judge_right_second_local_max(ind) or self.judge_right_second_local_min(ind)) and (self.judge_left_second_local_max(ind) or self.judge_left_second_local_min(ind)):
            lrmin_r = self.calculate_right_lrmin(ind)
            lrmin_l = self.calculate_left_lrmin(ind)
            dis_r = self.calculate_distance_right_local_ext(ind)
            dis_l = self.calculate_distance_left_local_ext(ind)
            if dis_l > dis_r:
                dis = dis_l
                lrmin = lrmin_l
                if dis < 0.5 * lrmin:
                    return "right"
                else:
                    return "?"
            else:
                dis = dis_r
                lrmin = lrmin_r
                if dis < 0.5 * lrmin:
                    return "left"
                else:
                    return "?"
        elif (self.judge_right_second_local_max(ind) or self.judge_right_second_local_min(ind)) and not (self.judge_left_second_local_max(ind) or self.judge_left_second_local_min(ind)):
            dis = self.calculate_distance_right_local_ext(ind)
            lrmin = self.calculate_right_lrmin(ind)
            if dis < 0.5 * lrmin:
                return "left"
            else:
                return "?"
        elif not (self.judge_right_second_local_max(ind) or self.judge_right_second_local_min(ind)) and (self.judge_left_second_local_max(ind) or self.judge_left_second_local_min(ind)):
            lrmin = self.calculate_left_lrmin(ind)
            dis = self.calculate_distance_left_local_ext(ind)
            if dis < 0.5 * lrmin:
                return "right"
            else:
                return "?"
        else:
            return "?"

    def first_round(self):
        """
        This is the first round.

        Do the judgement on each of the two adjacent characters whose
        relationship in mark_list is not sure.
        There are 16 different cases, and all the cases are handled according to
        the core judgement algorithm.
        """
        length = len(self.dts_list)
        for ind in range(length):
            if self.mark_list[ind] == 0:
                current_dts = self.dts_list[ind]
                current_mi = self.mi_list[ind]
                A = current_dts > self.dts_standard_derivation + self.dts_mean
                B = self.dts_mean < current_dts <= self.dts_standard_derivation + self.dts_mean
                C = -self.dts_standard_derivation + self.dts_mean < current_dts <= self.dts_mean
                D = current_dts <= self.dts_mean - self.dts_standard_derivation
                a = current_mi > self.mi_mean + self.mi_standard_derivation
                b = self.mi_mean < current_mi <= self.mi_mean + self.mi_standard_derivation
                c = self.mi_mean -self. mi_standard_derivation < current_mi <= self.mi_mean
                d = current_mi <= self.mi_mean - self.mi_standard_derivation
                if a or ( A and b ):  # Case: Aa or Ba or Ca or Da or Ab
                    self.mark_list[ind] = "bound"
                elif d or ( D and c ): # Case: Ad or Bd or Cd or Dd or Dc
                    self.mark_list[ind] = "separated"
                elif ( A and c ) or ( C and b ):  # Case: Ac or Cb
                    self.mark_list[ind] = self.case_Ac_or_Cb(ind)
                elif ( B and c ) or ( D and b ):  # Case: Bc or Db
                    self.mark_list[ind] = self.case_Bc_or_Db(ind)
                elif C and c:  # Case: Cc
                    self.mark_list[ind] = self.case_Cc(ind)
                elif B and b:  # Case: Bb
                    self.mark_list[ind] = self.case_Bb(ind)
                else:       # Other cases
                    self.mark_list[ind] = "?"
            else:
                pass

    def second_round(self):
        """
        This is the second round.

        This round will search all of the adjacent characters whose
        relationships are marked "?".
        """
        length = len(self.dts_list)
        for num in range(length):
            if self.mark_list[num] == "?":
                self.mark_list[num] = self.case_second_round(num)

    def third_round(self):
        """
        This is the third round.

        This round will search all of the adjacent characters whose
        relationships are marked "?".
        However, the means related to dtscore of the words are used up, so judge
        the relationship according to its mi value.
        """
        length = len(self.mark_list)
        for num in range(length):
            if self.mark_list[num] == "?":
                if self.mi_list[num] >= THETA:  # THETA is the mi valve parameter.
                    self.mark_list[num] = "bound"
                else:
                    self.mark_list[num] = "separated"
            else:
                pass

    def get_mark_list(self):
        self.first_round()
        self.second_round()
        self.third_round()
        return self.mark_list
