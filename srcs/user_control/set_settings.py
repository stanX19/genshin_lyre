try:
    from ...utils import return_mouse_coordinate
    from ...utils import print_rows as print_list
    from ...classes import Settings
    import controller
except ImportError:
    from utils import return_mouse_coordinate
    from utils import print_rows as print_list
    from classes import Settings
    import controller

def set_settings(enter:str):
    enter = enter.replace("set",'').strip()
    i = 0
    Settings_dict = controller.settings.get_dict()
    while i < 1:
        if 'coordinate' in enter:
            Settings.genshin_app_coordinate = return_mouse_coordinate("genshin_app position")
            controller.settings.save()
            print(f"  genshin_app position is set to {Settings.genshin_app_coordinate}\n")
            break
        elif enter in Settings_dict:
            ori_val = Settings_dict[enter]
            value_class = type(ori_val)
            if value_class != bool:
                print(f"  Current {enter} is set to \"{ori_val}\"")
                new_value = input(f"new value for {enter}?({value_class.__name__}): ")
                try:
                    new_value = value_class(new_value)
                    print(f"  {enter} set to {new_value}")
                except ValueError:
                    print("invalid value")
                    break
            else:
                print(f"  {enter} is currently turned {'on' if ori_val else 'off'}")
                toggle_value = input(f"turn {enter} {'off' if ori_val else 'on'}?(Y/n): ").lower() == "y"
                new_value = (toggle_value + ori_val) == 1  # xor, plot it yourself
                if toggle_value:
                    print(f"  {enter} is turned {'on' if new_value else 'off'}")
                else:
                    print("  Cancelled\n")
                    break
            #       object    attr   value
            setattr(Settings, enter, new_value)
            controller.settings.save()
            break
        else:
            print("enter 'q' to quit this mode")
            print_list(list(Settings_dict), False, ")", "  ", "")
            command = input("Which users settings do you want to edit?: ").lower()
            if command.isnumeric():
                try:
                    enter = list(Settings_dict)[int(command) - 1]
                except ValueError as exc:
                    print(f"ERROR: Please input whole numbers")
                i -= 1
            else:
                enter = command
        i += 1