from typing import TypeVar, Callable
from brick_simulation import brick_simulation

T = TypeVar('T')

def get_input(field_name: str, cast_func: Callable[[str], T], indent: int = 0) -> T:
    prompt = indent * "\t" + field_name + ": "
    error_msg = indent * "\t" + "Please enter a valid number."

    while True:
        try:
            return cast_func(input(prompt))
        except ValueError:
            print(error_msg)


def brick_simulation_menu():
    while True:
        print("\nElastic Collision Simulation")

        print("\nEnter simulation parameters:")
        print("Brick 1:")
        mass_one = get_input("mass [kg]", float, 1)
        velocity_one = get_input("velocity [m/s]", float, 1)
        print("Brick 2:")
        mass_two = get_input("mass [kg]", float,1)
        velocity_two = get_input("velocity [m/s]", float, 1)

        print("\nSimulation started in a new window.")
        print("Close the window to return to the menu.")

        brick_simulation(
            mass_one,
            mass_two,
            velocity_one,
            velocity_two,
        )

        run_again = input("\nDo you want to run the simulation again? (Y/n): ")
        if run_again.lower() == "n":
            break
