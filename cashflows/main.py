import fire
import json 

from Util import InvestmentProject


class Main(object):
    
    @staticmethod
    def describe_investment(filepath, hurdle_rate=None):
        investment_project = InvestmentProject.from_csv(filepath=filepath, hurdle_rate=hurdle_rate)
        description = investment_project.describe()
        print(json.dumps(description, indent=4))

    @staticmethod
    def plot_investment(filepath, save="", show=False, hurdle_rate=None):
        investment_project = InvestmentProject.from_csv(filepath=filepath, hurdle_rate=hurdle_rate)
        fig = investment_project.get_plot(show=show)
        if save:
            fig.savefig(save)
        

if __name__ == "__main__":
    fire.Fire(Main)
    
