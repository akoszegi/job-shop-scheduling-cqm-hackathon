import pathlib
import click

from src.generate_charts import generate_gantt_chart, generate_output_table, get_empty_figure, get_minimum_task_times
from src.job_shop_scheduler import run_shop_scheduler
from src.model_data import JobShopData

from app_configs import (
    RESOURCE_NAMES,
    SCENARIOS,
)

BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("input").resolve()


def generate_unscheduled_gantt_chartt(scenario: str):
    model_data = JobShopData()
    model_data.load_from_file(DATA_PATH.joinpath(SCENARIOS[scenario]), resource_names=RESOURCE_NAMES)
    df = get_minimum_task_times(model_data)
    fig = generate_gantt_chart(df)

@click.command()
@click.option("-i", "--input_size", default="10x10",
              type=str,
              help="Path to configuration file to use for the problem suite.")
@click.option("-t", "--time_limit", default=10,
              type=int,
              help="Path to configuration file to use for the problem suite.")
# @click.option("-c", "--config", default=DEFAULT_CONFIG_FILE,
#               type=str,
#               help="Path to configuration file to use for the problem suite.")
def main(input_size, time_limit):

    # To go in yaml file
    filename = SCENARIOS[input_size]
    time_limit = time_limit

    # Load input data
    model_data = JobShopData()
    model_data.load_from_file(DATA_PATH.joinpath(filename), resource_names=RESOURCE_NAMES)

    # BUild model and solve
    results = run_shop_scheduler(
        model_data,
        solver_time_limit=time_limit,
        use_mip_solver=False,
        allow_quadratic_constraints=(True),
        out_sol_file=input_size + 'output.txt', # TODO: what directory should this be saved in?
        out_plot_file=input_size + 'plot.png' # TODO: what directory should this be saved in?
    )

if __name__ == '__main__':
    main()