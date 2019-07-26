class StatMinMaxAvg:

    stat_name   = ""
    num_entries = 0
    total       = 0
    min_value   = 9999
    max_value   = -9999
    average     = 0.
    values      = [] # I may get rid of this for memory reasons if it's never used

    def __init__(self, name):
        self.stat_name = name

    # allow overwrite of name
    def set_stat_name(self,name):
        self.stat_name = name
    
    # add a new entry to the stat tracker
    def add_entry(self,value):
        self.values.append(value)
        self.num_entries += 1
        self.total += value
        
        # update calculated values
        if value < self.min_value:
            self.min_value = value
        elif value > self.max_value:
            self.max_value = value

        if not self.num_entries == 0: # this should never happen, but you never know
            self.average = float(self.total)/self.num_entries
        else:
            self.average = 0.
        
    # get values
    def get_stat_name(self):
        return self.stat_name
    def get_num_entries(self):
        return self.num_entries
    def get_total_value(self):
        return self.total
    def get_min_value(self):
        return self.min_value
    def get_max_value(self):
        return self.max_value
    def get_average(self):
        return self.average

    # fancy print
    def to_string(self):
        out = "Tracking stat {} -- Total: {} | Min: {} | Max: {} | Avg: {} -- from {} entries".format(self.stat_name,self.total,self.min_value,self.max_value,self.average,self.num_entries)
        return out

    def to_csv(self):
        out = "{};{};{};{};{};{}".format(self.stat_name,
                                         self.num_entries,
                                         self.total,
                                         self.min_value,
                                         self.max_value,
                                         self.average)
        return out

    def to_cfg(self):
        out  = "stat_name\t= {}\n"  .format(self.stat_name)
        out += "num_entries\t= {}\n".format(self.num_entries)
        out += "total\t\t= {}\n"    .format(self.total)
        out += "min_value\t= {}\n"  .format(self.min_value)
        out += "max_value\t= {}\n"  .format(self.max_value)
        out += "average\t\t= {}\n"  .format(self.average)
        return out
