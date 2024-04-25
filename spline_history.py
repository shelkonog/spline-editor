

class SplineHistory:
    max_length = 5
    list_splines = []
    cur_spline_index: int = 0

    def save_spline(self, value):
        self.copy_list = value[:]

        if self.cur_spline_index != len(self.list_splines) - 1:
            self.list_splines = self.list_splines[:self.cur_spline_index + 1]
            self.cur_spline_index = len(self.list_splines) - 1

        if self.cur_spline_index == self.max_length:
            self.list_splines.pop(0)
            self.list_splines.append(self.copy_list)
        else:
            self.list_splines.append(self.copy_list)
            self.cur_spline_index = len(self.list_splines) - 1

    def copy_spline(self, index):
        return self.list_splines[index].copy()
