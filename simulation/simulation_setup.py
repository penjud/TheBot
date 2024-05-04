from flumine import Flumine, clients, Backtest
from flumine.controls.loggingcontrols import LoggingControl
from strategy import BacktestStrategy  # Assuming this is defined in a separate 'strategy.py' file

def setup_simulation():
    client = clients.SimulatedClient()
    framework = Flumine(client=client)
    strategy = BacktestStrategy()
    framework.add_strategy(strategy)
    return framework

if __name__ == "__main__":
    simulation = setup_simulation()
    simulation.run()
