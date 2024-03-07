from tkinter import messagebox as mb


class messages:
    def __init__(self, type : str = "error", message : str = None):
        """"
        Constructor for the messages class
        :param type: the type of the message box : error, info, move
        :param message: the message to be displayed
        """
        self.message = message
        self.type = type

    def display(self):
        """
        Displays the right message box based on the type
        :return:
        """
        if self.type == "error":
            self.display_error(self.message)
        elif self.type == "info":
            self.display_info(self.message)
        elif self.type == "move":
            self.display_move()

    def display_error(self, error : str):
        """
        Displays an error message box, if no message provided, it will display a default message
        :param error:
        """
        if error == None:
            message = "An error has occured!"
        else:
            message = f"An error has occured: {error}"

        mb.showerror("Error", message)
    #Displays an info message box, if no message provided, it will display a default message
    def display_info(self, info : str):
        """
        Displays an info message box, if no message provided, it will display a default message
        :param info:
        """
        if info == None:
            message = "Somebody forgot to write a message here!"
        else:
            message = f"{info}"

        mb.showinfo("Info", message)

    def display_move(self):
        """
        Displays a message box for a move, if no message provided, it will display a default message
        :param move:
        """
        message = "Illegal Move!"

        mb.showinfo("Move", message)


    def set_message(self, message : str):
        """
        Sets the message to be displayed
        :param message:
        """
        self.message = message

    def set_type(self, type : str):
        """
        Sets the type of the message box
        :param type:
        """
        self.type = type


