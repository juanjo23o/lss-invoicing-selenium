class HelpMyLocator:

    @staticmethod
    def identify_index(account_name):
        index = None
        proper_account_index = account_name.split("-")
        try:
            index = proper_account_index[1]
            return int(index)
        except:
            return index
