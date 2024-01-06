#Importing the required modules such as the
#random module, regex module, sqlite3
#module for sql commands, hashlib module
#for a hashing algorithm & csv module for writing
#to files inlcuding the tkinter module for the interface
import random,re,sqlite3,hashlib,csv
from tkinter import *                                             
import tkinter.ttk as ttk                                                                                     
from tkinter import messagebox
from tkinter import filedialog


#Setting up fixed variables which are used throughout
#the program such as the logo image, the database name,
#an email regex check and the different colors used
#in the interface 
IMAGE = 'LogoImage.gif'
DATABASE = 'FlashQuiz.db'
REGEX = r"^[a-zA-Z0-9._-]+\@[a-zA-Z0-9]+(\.[a-z]+){1,2}$"
COLORS = ['#E79214','#2E2928','#CF0A0A']  #Orange,Dark,Red


#The main parent class, Window, from which
#all the others classes inherit from
class Window():
        #Initialize all the attributes for all the classes
        #such as the the window, the canvas, the UserID and CatID
        #which are set to a None value if the user hasn't signed-up
        #or logged-in yet and a protocol set for all windows
        #to prompt a message box when closing the window
    def __init__(self,frmNew,UserID=None,CatID=None):
        self.frmNew = frmNew
        self.BackCanvas = None
        frmNew.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.UserID = UserID
        self.CatID = CatID

        #Method to set the dimensions of the windows
        #where the height & width are passed on as arguements 
    def windowDimension(self,width,height):                          
        screenWidth = self.frmNew.winfo_screenwidth()                
        screenHeight = self.frmNew.winfo_screenheight()                 
        x = (screenWidth - width) / 2                                   
        y = (screenHeight - height) / 2
        self.frmNew.geometry('%dx%d+%d+%d' % (width,height,x,y))
        self.frmNew.resizable(0,0)

        #Method that creates the canvas for all the windows
        #setting all the same attributes for their canvas
    def CanvasSetUp(self):                                                                     
        self.BackCanvas = Canvas(self.frmNew,background = COLORS[0],highlightthickness=0)
        self.BackCanvas.place(x=0,y=0,width = 1000,height = 700)

        #Method that runs when the window is closed where
        #a messagebox is shown asking whether to quit or not
    def closeWindow(self):                                                                     
        getExit = messagebox.askyesno(title="Quit",message="Are you sure you want to quit?")   
        if getExit > 0:                                                                        
            self.frmNew.destroy()                                   
        return

        #Switching windows method where the name of the new class and its attributes
        #are passed on as arguements where the current window is destroyed and opens
        #the new window
    def SwitchWindow(self,Window,Attributes=None):
        self.frmNew.destroy()
        newWindow = Tk()
        if Attributes:
            extra = Window(newWindow,*Attributes)
        else:
            extra = Window(newWindow)       
        
#The MainMenu class which inherits from Window and allows user
#to log in or sign up and includes an image of the logo
class MainMenu(Window):
        #Initialize all the attributes for the class
        #such as the buttons for login-in and signing-up
        #and the image used for the logo 
    def __init__(self,frmFirst):                                        
        Window.__init__(self,frmFirst)                                  
        self.frmFirst = frmFirst                                        
        self.windowDimension(1000,700)                                                                   
        frmFirst.title("FlashQuiz")                                    
        self.CanvasSetUp()
        #The buttons also use the lambda function in order to
        #prevent the command of the button being runned before
        #it is actually pressed where the command is to switch
        #to the other window
        self.btnLogIn = Button(frmFirst,text='Log in',width=10,background = COLORS[1],fg =COLORS[0],font=('Berlin Sans fb demi',28),
                               bd=0,command= lambda :self.SwitchWindow(LogIn)).place(y = ((700 / 2) + 240),relx = 0.5,anchor = CENTER)
        self.btnSignUp = Button(frmFirst,text='Sign up',width=10,background = COLORS[1],fg =COLORS[0],font=('Berlin Sans fb demi',28),
                                bd=0,command= lambda :self.SwitchWindow(SignUp)).place(y = ((700 / 2) + 140),relx = 0.5,anchor = CENTER)
        self.imgLogo = PhotoImage(file=IMAGE)
        self.background = self.BackCanvas.create_image((1000 / 2),230,image=self.imgLogo)

#The SignUp class which also inherits from Window
#and allows the user to sign-up for an account
class SignUp(Window):
        #Initialize all the attributes
        #of the class which include multiple
        #labels for the details as well as
        #multiple corresponding entries
        #to get the user's details
    def __init__(self,frmSignUp):                       
        Window.__init__(self,frmSignUp)                 
        self.windowDimension(1000,700)                  
        frmSignUp.title('Sign Up')                      
        self.CanvasSetUp()
        #The binding function is used to bind the enter key
        #to run the AddUser method whenever the user
        #presses the enter key
        frmSignUp.bind('<Return>',self.AddUser)
        #Three buttons where the LogIn button allows the user to
        #switch back to the LogIn screen and the SignUp2 button to
        #sign up for an account
        self.btnLogIn = Button(frmSignUp,text='Log in',width=10,background = COLORS[1],fg =COLORS[0],font=('Berlin Sans fb demi',28),
                               bd=0,command = lambda : self.SwitchWindow(LogIn))                               
        self.btnLogIn.place(y = ((700 / 2) - 240),relx = 0.45,anchor = E)
        self.btnSignUp = Button(frmSignUp,text='Sign up',width=10,background = COLORS[1],fg =COLORS[0],font=('Berlin Sans fb demi',28)
                                ,bd=0,state=DISABLED)
        self.btnSignUp.place(y = ((700 / 2) - 240),relx = 0.55,anchor = W)
        self.btnSignUp2 = Button(frmSignUp,text='Sign up',width=10,background = COLORS[2],fg =COLORS[0],font=('Arial Rounded MT Bold',28),
                                 bd=0,command=self.AddUser)
        self.btnSignUp2.place(y = ((700 / 2) + 300),relx = 0.5,anchor = CENTER)
        self.lblFirstname = Label(frmSignUp,text='Firstname:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblFirstname.place(x=40,y=220)
        self.entryFirstname = Entry(frmSignUp,width = 18,font=('Calibri',22),fg=COLORS[1])
        self.entryFirstname.place(x=220,y=223)
        self.lblSecondname = Label(frmSignUp,text='Secondname:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblSecondname.place(x=40,y=320)
        self.entrySecondname = Entry(frmSignUp,width = 18,font=('Calibri',22),fg=COLORS[1])
        self.entrySecondname.place(x=220,y=323)
        self.lblEmail = Label(frmSignUp,text='E-mail:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblEmail.place(x=40,y=420)
        self.entryEmail = Entry(frmSignUp,width = 18,font=('Calibri',22),fg=COLORS[1])
        self.entryEmail.place(x=220,y=423)
        self.lblAge = Label(frmSignUp,text='Age:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblAge.place(x=40,y=520)
        self.entryAge = Spinbox(frmSignUp,from_=10, to=99,width = 17,font=('Calibri',22),fg=COLORS[1])
        self.entryAge.place(x=220,y=523)
        self.lblUsername = Label(frmSignUp,text='Username:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblUsername.place(x=550,y=220)
        self.entryUsername = Entry(frmSignUp,width = 18,font=('Calibri',22),fg=COLORS[1])
        self.entryUsername.place(x=700,y=223)
        self.lblPassword = Label(frmSignUp,text='Password:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblPassword.place(x=550,y=320)
        self.entryPassword = Entry(frmSignUp,width = 18,font=('Calibri',22),fg=COLORS[1])#,show='*'
        self.entryPassword.place(x=700,y=323)
        self.lblReenter1 = Label(frmSignUp,text='Re-enter',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblReenter1.place(x=550,y=438)
        self.lblReenter2 = Label(frmSignUp,text='password:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblReenter2.place(x=550,y=478)
        self.entryReenter = Entry(frmSignUp,width = 18,font=('Calibri',22),fg=COLORS[1])#,show='*'
        self.entryReenter.place(x=700,y=481)

        #The AddUser method which creates an empty array(UserDetails)
        #where it appends the user's details from the entry boxes if the
        #ValidateData method return True. It then runs the fnAddtotblUsers
        #function where it adds the details to the database
    def AddUser(self,event=None):                                                   
        UserDetails = []                                                             
        if self.ValidateData():
            UserDetails.append(self.entryUsername.get())                            
            UserDetails.append(fnGetHashValue(self.entryPassword.get()))             
            UserDetails.append(self.entryEmail.get())                               
            UserDetails.append(self.entryFirstname.get().title())                   
            UserDetails.append(self.entrySecondname.get().title())              
            UserDetails.append(int(self.entryAge.get()))
            self.UserID = fnAddtotblUsers(UserDetails)   
            self.SwitchWindow(SetsViewer,[self.UserID])

        #The ValidateData method is used to validate all the user's entries
        #in case any abnormal data in entered and shows a messagebox
        #indicating if the details are not validated
    def ValidateData(self):                                                           
        if not self.entryFirstname.get() or len(self.entryFirstname.get()) > 50:      
            messagebox.showerror('Error','Provide a valid firstname')                 
            return False                                                              
        elif not self.entrySecondname.get() or len(self.entrySecondname.get()) > 50:
            messagebox.showerror('Error','Provide a valid secondname')
            return False
            #The e-mail validation uses the regular expression which is set
            #at the start of the program in order to check the format of the e-mail
        elif not self.entryEmail.get() or len(self.entryEmail.get()) > 50 or not(re.match(REGEX,self.entryEmail.get())):
            messagebox.showerror('Error','Provide a valid e-mail address')
            return False
        elif not self.entryAge.get().isdigit() or int(self.entryAge.get()) > 99 or int(self.entryAge.get()) < 10:
            messagebox.showerror('Error','Invalid age')
            return False
        elif not self.entryUsername.get() or len(self.entryUsername.get()) > 50:  
            messagebox.showerror('Error','Provide a valid username')
            return False
            #The username validation checks in the database if the username entered
            #doesn't match any other usernames and if not, a messagebox is prompted
        elif any(self.entryUsername.get() in x for x in fnFetchAllUsers()):
            messagebox.showerror('Error','Username already taken')
            return False
            #A regular expression to check the password format is used
            #whether it meets the requirements as well as other checks such as
            #its length and if it doesn't meet the requirements, two messageboxes are shown
            #where one of them shows the details of the password format required
        elif not self.entryPassword.get() or len(self.entryPassword.get()) < 8 or not (re.search(r"[A-Z].*\d|\d.*[A-Z]",self.entryPassword.get())):
            messagebox.showerror('Error','Provide password in correct format')
            messagebox.showinfo('Password Format','A password has to be longer than 8 characters including an uppercase letter and a number')
            return False
        elif self.entryReenter.get() != self.entryPassword.get():
            messagebox.showerror('Error',"Passwords don't match")
            return False
        return True

#The LogIn class inherits from Window and
#lets the user to log in with their
#existing account
class LogIn(Window):
        #Initialize all the attributes
        #of the class which include three buttons and
        #two labels which correspond to the two entries
        #for the user's username & password
    def __init__(self,frmLogIn):                     
        Window.__init__(self,frmLogIn)               
        self.frmLogIn = frmLogIn
        self.windowDimension(1000,700)
        frmLogIn.title("Log In")
        self.CanvasSetUp()
        #The binding function is used to bind the enter key
        #to run the UserLogIn method whenever the user
        #presses the enter key
        frmLogIn.bind('<Return>',self.UserLogIn)
        #Three buttons where the SignUp button allows the user to
        #switch back to the SignUp screen and the LogIn button to
        #log in with an account
        self.btnLogIn = Button(frmLogIn,text='Log in',width=10,background = COLORS[1],fg =COLORS[0],font=('Berlin Sans fb demi',28)
                               ,bd=0,state=DISABLED)
        self.btnLogIn.place(y = ((700 / 2) - 240),relx = 0.45,anchor = E)
        self.btnLogIn2 = Button(frmLogIn,text='Log in',width=10,background = COLORS[2],fg =COLORS[0],font=('Arial Rounded MT Bold',28),
                                bd=0,command = self.UserLogIn)
        self.btnLogIn2.place(y = ((700 / 2) + 300),relx = 0.5,anchor = CENTER)
        self.btnSignUp = Button(frmLogIn,text='Sign up',width=10,background = COLORS[1],fg =COLORS[0],font=('Berlin Sans fb demi',28),
                                bd=0,command = lambda : self.SwitchWindow(SignUp))
        self.btnSignUp.place(y = ((700 / 2) - 240),relx = 0.55,anchor = W)
        self.lblUsername = Label(frmLogIn,text='Username:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',26))
        self.lblUsername.place(x=230,y=320)
        self.entryUsername = Entry(frmLogIn,width = 22,font=('Calibri',22),fg=COLORS[1])
        self.entryUsername.place(x=410,y=323)
        self.lblPassword = Label(frmLogIn,text='Password:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',26))
        self.lblPassword.place(x=230,y=420)
        self.entryPassword = Entry(frmLogIn,width = 22,font=('Calibri',22),fg=COLORS[1])#,show='*'
        self.entryPassword.place(x=410,y=423)
        #The Forgot button allows the user to change their password
        #if they forgot it by running the ForgotPassword method
        self.lblForgot = Button(frmLogIn,text="Forgot password?",width=15,bg=COLORS[0],fg='Blue',font=('Georgia',20,'underline'),bd=0
                                ,command=self.ForgotPassword,activebackground=COLORS[0])
        self.lblForgot.place(y=((700 / 2) +200),relx = 0.5, anchor=CENTER)

        #Method that opens a TopLevel window
        #for the user to change their password
    def ForgotPassword(self):
        newWindow = Toplevel(self.frmNew)
        self.top_level = PasswordReset(newWindow)

        #Method that opens the SetsViewer window if
        #the CheckLogIn method returns True
    def UserLogIn(self,event=None):
        if self.CheckLogIn(self.entryUsername.get(),self.entryPassword.get()):      
            self.SwitchWindow(SetsViewer,[self.UserID])                          

        #The CheckLogIn method fetches all the users' details
        #from the database and compares all the usernames and hash values
        #of the passwords with the username entry and the hash value created 
        #from the password entry with the GetHashValue function, if they match,
        #it return True otherwise shows a messagebox showing an error
    def CheckLogIn(self,Username,Password):                                        
        Users = fnFetchAllUsers()       
        for x in Users:                                                           
            if Username == x[1] and fnGetHashValue(Password) == x[2]:             
                self.UserID = x[0]                                                  
                return True                                                       
        messagebox.showerror('Error','Incorrect log in details provided. Try again')
        return False

#The PasswordReset class inherits from Window
#and lets the user to change their password
#if they forgot it by verifying their details first
class PasswordReset(Window):
    def __init__(self,frmPasswordReset):
        Window.__init__(self,frmPasswordReset)
        self.windowDimension(600,500)
        frmPasswordReset.title("Sets Viewer")
        self.CanvasSetUp()
        self.BackArrow = PhotoImage(file='Back-Arrow.gif')
        self.btnBack = Button(frmPasswordReset,command=self.Return,image=self.BackArrow,borderwidth=0,highlightthickness=0)
        self.btnBack.place(x=8,y=4)
        #The first frame that has multiple labels and corresponding entries
        #to check the user's details
        self.frmDetails = Frame(frmPasswordReset,bg=COLORS[0],bd=0,height=420,width=500)
        self.lblUsername = Label(self.frmDetails,text='Username:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',26))
        self.lblUsername.place(y=20)
        self.entryUsername = Entry(self.frmDetails,width = 18,font=('Calibri',22),fg=COLORS[1])
        self.entryUsername.place(x=225,y=20)
        self.lblEmail = Label(self.frmDetails,text='E-mail:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',26))
        self.lblEmail.place(y=100)
        self.entryEmail = Entry(self.frmDetails,width = 18,font=('Calibri',22),fg=COLORS[1])
        self.entryEmail.place(x=225,y=100)
        self.lblAge = Label(self.frmDetails,text='Age:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',26))
        self.lblAge.place(y=180)
        self.entryAge = Spinbox(self.frmDetails,from_=10, to=99,width = 17,font=('Calibri',22),fg=COLORS[1])
        self.entryAge.place(x=225,y=180)
        self.lblSecondName = Label(self.frmDetails,text='Secondname:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',26))
        self.lblSecondName.place(y=260)
        self.entrySecondName = Entry(self.frmDetails,width = 18,font=('Calibri',22),fg=COLORS[1])
        self.entrySecondName.place(x=225,y=260)
        self.btnVerify = Button(self.frmDetails,text='Verify',command=self.VerifyDetails,width=8,background = COLORS[2],fg =COLORS[0],font=('Arial Rounded MT Bold',28),bd=0)
        self.btnVerify.place(y=390,relx = 0.5,anchor = CENTER)
        #The second frame allows the user to change their password if
        #their details were verified from the first frame
        self.frmChange = Frame(frmPasswordReset,bg=COLORS[0],bd=0,height=420,width=500)
        self.lblNewPassword = Label(self.frmChange,text='New Password:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',25))
        self.lblNewPassword.place(y=80)
        self.entrNewPassword = Entry(self.frmChange,width = 18,font=('Calibri',22),fg=COLORS[1])
        self.entrNewPassword.place(y=80,x=225)#,show='*'
        self.lblRetype = Label(self.frmChange,text='Re-enter \nPassword:',justify=LEFT,bg=COLORS[0],fg=COLORS[1],font=('Georgia',25))
        self.lblRetype.place(y=200)
        self.entrReenter = Entry(self.frmChange,width = 18,font=('Calibri',22),fg=COLORS[1])
        self.entrReenter.place(y=240,x=225)#,show='*'
        self.btnChange = Button(self.frmChange,text='Change',command=self.ChangePassword,width=8,background = COLORS[2],fg =COLORS[0],font=('Arial Rounded MT Bold',28),bd=0)
        self.btnChange.place(y=390,relx = 0.5,anchor = CENTER)
        #Sets the current frame as the first frame, frmDetails which is 
        #changed if the details are verified
        self.CurrentFrame = self.frmDetails
        self.CurrentFrame.place(x=50,y=50)
        frmPasswordReset.grab_set()

        #The ValidateEntries method gets all the entries and validates them
        #in case there is any abnormal data entered and shows a messagebox
        #showing an error and returning False
    def ValidateEntries(self):
        if not self.entryUsername.get() or len(self.entryUsername.get()) > 50:
            messagebox.showerror('Error','Provide a valid username')
            return False
        elif not self.entryEmail.get() or len(self.entryEmail.get()) > 50 or not(re.match(REGEX,self.entryEmail.get())):
            messagebox.showerror('Error','Provide a valid e-mail address')
            return False
        elif not self.entryAge.get().isdigit() or (int(self.entryAge.get()) > 99 or int(self.entryAge.get()) < 10):
            messagebox.showerror('Error','Invalid age')
            return False
        elif not self.entrySecondName.get() or len(self.entrySecondName.get()) > 50:
            messagebox.showerror('Error','Provide a valid secondname')
            return False
        return True

        #The VerifyDetails method runs if the ValidateEntries
        #method returns True and compares all the details entered
        #to all the details in the database for all the users,
        #if they don't match, a messagebox is shown and returns
        #otherwise it changes to the second frame to ask for the
        #new password
    def VerifyDetails(self):
        if self.ValidateEntries():
            Match = True
            Details = fnFetchUserDetails(self.entryUsername.get())[0]
            if Details:
                if not(self.entryEmail.get() == Details[3]):
                    messagebox.showerror('Incorrect Details','Incorrect details provided')
                    return
                elif not(int(self.entryAge.get()) == Details[6]):
                    messagebox.showerror('Incorrect Details','Incorrect details provided')
                    return
                elif not(self.entrySecondName.get() == Details[5]):
                    messagebox.showerror('Incorrect Details','Incorrect details provided')
                    return
                self.CurrentFrame.place_forget()
                self.CurrentFrame = self.frmChange
                self.CurrentFrame.place(x=50,y=50)
            else:
                messagebox.showerror('Not found','No user found')
                return

        #The ChangePassword method checks the format of the password entered
        #and returns False is it doesn't match or if the both passwords entered
        #twice don't match. Otherwise the password for the user is updated
        #in the database by passing the hash value of the password to the
        #fnGetHashValue function and closing the window returning to the
        #log in screen
    def ChangePassword(self):
        if not self.entrNewPassword.get() or len(self.entrNewPassword.get()) < 8 or not (re.search(r"[A-Z0-9]",self.entrNewPassword.get())):   ####The regex doesn't work?
            messagebox.showerror('Error','Provide password in correct format')
            messagebox.showinfo('Password Format','A password has to be longer than 8 characters including an uppercase letter and a number')
            return False
        elif self.entrNewPassword.get() != self.entrReenter.get():
            messagebox.showerror('Error',"Passwords don't match")
            return False
        fnUpdatePassword(fnGetHashValue(self.entrNewPassword.get()),self.entryUsername.get())
        messagebox.showinfo('Password Updateed','Password changed successfully')
        self.frmNew.grab_release()
        self.frmNew.destroy()

        #The Return method is used when the
        #Back button is pressed to return to the
        #log in screen
    def Return(self):
        self.frmNew.grab_release()
        self.frmNew.destroy()
        
#The SetsViewer class inherits from Window
#and allows the user to view their current sets
#and also has a button in case they want to create
#a new set of queations.
class SetsViewer(Window):                              
    def __init__(self,frmSetsViewer,UserID):            
        Window.__init__(self,frmSetsViewer,UserID)     
        self.windowDimension(1000,700)                 
        frmSetsViewer.title("Sets Viewer")             
        self.CanvasSetUp()
        #Empty array which holds all the buttons
        #for each set
        self.Buttons = []
        self.Title = Label(frmSetsViewer,text='Quizzes',bg=COLORS[0],fg=COLORS[1],font=('Forte',40)).place(relx=0.08,rely=0.08,anchor='nw')
        self.Line = self.BackCanvas.create_line(70,140,930,140, fill="#2E2928", width=5)
        #A canvas is created in the window where all the buttons are placed
        #which also allows the user to scroll through the buttons
        #if there's more than eight sets
        self.Canvas = Canvas(frmSetsViewer,background = COLORS[0],highlightthickness=0)
        self.Canvas.place(x=70,y=160,height=470,width=860)
        self.Frame = Frame(self.Canvas,bg=COLORS[0],bd=0,height=470,width=860)
        self.Frame.place(x=0,y=0)
        #The AddButton allows the user to create a new set
        #of questions
        self.AddButton = Button(self.Frame,text="+\nAdd Quiz",width = 11,height=3,background = COLORS[1],command=lambda : self.SwitchWindow(QuestionsEditor,[True,self.UserID])
                                ,fg ='white',bd=0,font=('Berlin Sans fb demi',28))#.place(x=0,y=0)
        self.Buttons.append(self.AddButton)
        self.Categories = fnFetchCategoriesUsers(self.UserID)
        #Runs the AddButtons method which adds all the buttons
        #for each category fetched from the database in the previous line
        self.AddButtons(self.Buttons,self.Categories)
        self.Scrollbar = ttk.Scrollbar(frmSetsViewer, orient="vertical", command=self.Canvas.yview)
        self.Canvas.configure(yscrollcommand=self.Scrollbar.set)
        self.Scrollbar.pack(side=RIGHT, fill = Y)
        self.Canvas.create_window((0, 0), window=self.Frame, anchor="nw")
        #Binds the scrollbar created to the canvas and the frame to scroll through
        #all the buttons of the sets
        self.Frame.bind('<Configure>',lambda e : self.Canvas.configure(scrollregion=self.Canvas.bbox("all")))
        self.Canvas.bind_all('<MouseWheel>',self.MouseWheel)

        #MouseWheel method that lets the user scroll in the
        #y-direction of the canvas by the units specified
    def MouseWheel(self,event):
        self.Canvas.yview_scroll(int(-1*(event.delta/120)),'units')

        #The AddButtons method creates a button for each
        #set of questions and places them in set rows
        #and columns of the frame
    def AddButtons(self,Buttons,Categories):             #Method that creates an 
        for x in Categories:                             #array of Buttons for all
            i = x[0]                                     #of the user's sets
            self.CatID = x[2]
            self.button = Button(self.Frame,text=i,width = 11,height=3,command=lambda x=x,ID=self.CatID:self.SwitchWindow(QuestionsEditor,[False,self.UserID,x,ID])
                                 ,background = COLORS[1],fg ='white',bd=0,font=('Berlin Sans fb demi',28),wraplength=185)
            Buttons.append(self.button)

        for j, button in enumerate(Buttons):
            self.Frame.columnconfigure(j % 3)
            button.grid(row=j // 3, column=j % 3,ipadx=5,ipady=5,padx=20,pady=7)
                
#The QuestionEditor class inherits from Window
#which lets the user to start the quiz or make
#any changes to it as well as view all the questions inside that set 
class QuestionsEditor(Window):
        #Initialize all the attributes
        #where New,UserID,Category and CatID are passed
        #and New is a boolean value and shows if it's a new
        #set of questions if New is set to True
    def __init__(self,frmQuestionEditor,New,UserID,Category=None,CatID = None):
        Window.__init__(self,frmQuestionEditor,UserID,CatID)
        self.windowDimension(1000,700)
        frmQuestionEditor.title("Question Editor")
        self.CanvasSetUp()
        self.New = New
        self.Category = Category
        self.Questions = []
        self.SelectedQuestion = None
        self.Ordered = False
        self.Recent_Score = (self.Category[1] if self.Category is not None and self.Category[1] else '-')
        #Creates an entry box for the title of the set if it's
        #a new set otherwise creates a label with the Category
        #name of the set
        if self.New:
            self.CatTitle = StringVar(value='Quiz Title')
            self.Subject = Entry(frmQuestionEditor,fg=COLORS[1],bd=0,font=('Calibri',20),textvariable=self.CatTitle)
            self.Subject.place(x=50,y=45,anchor='nw',width=450)
        else:
            self.Subject = Label(frmQuestionEditor,text=self.Category[0],bg = COLORS[0],fg =COLORS[1],font=('Forte',40,'underline'))
            self.Subject.place(x=50,y=30,anchor='nw')
        self.Line = self.BackCanvas.create_line(50,130,940,130, fill="#2E2928", width=5)
        self.Search = StringVar(value='Search')
        #An entry box to search all the questions
        #in the table
        self.entrSearch = Entry(frmQuestionEditor,fg=COLORS[1],textvariable=self.Search,bd=0,font=('Calibri',14),width=43)
        self.entrSearch.place(x=508,y=134)
        self.lblRecentScore = Label(frmQuestionEditor,text=(f"Recent Score: {self.Recent_Score}%"),bg=COLORS[0],fg=COLORS[1],font=('Berlin Sans fb demi',25))
        self.lblRecentScore.place(x=503,y=40)
        self.lblAverageDifficulty = Label(frmQuestionEditor,bg=COLORS[0],fg=COLORS[1],font=('Berlin Sans fb demi',22))
        self.lblAverageDifficulty.place(x=503,y=89)
        self.BackArrow = PhotoImage(file='Back-Arrow.gif')
        self.btnBack = Button(frmQuestionEditor,image=self.BackArrow,command=lambda:self.SwitchWindow(SetsViewer,[self.UserID]),borderwidth=0,highlightthickness=0)
        self.btnBack.place(x=8,y=4)
        self.btnStart = Button(frmQuestionEditor,text='Start!',width=7,command=self.Start,bg =COLORS[1],fg =COLORS[0]
                               ,font=('Berlin Sans fb demi',25),bd=0)
        self.btnStart.place(x=801,y=40)
        self.btnNew = Button(frmQuestionEditor, text='New',background = COLORS[2],fg =COLORS[0],command=self.AddQuestion
                             ,width=7,font=('Arial Rounded MT Bold',20),bd=0).place(x=50,y=590)
        self.btnEdit = Button(frmQuestionEditor, text='Edit',command = self.EditQuestion,background = COLORS[2]
                              ,fg =COLORS[0],width=7,font=('Arial Rounded MT Bold',20),bd=0).place(x=270,y=590)
        self.btnExport = Button(frmQuestionEditor, text='Export',command=self.ExportQuestions,background = COLORS[2]
                              ,fg =COLORS[0],width=7,font=('Arial Rounded MT Bold',20),bd=0).place(x=815,y=590)
        self.btnDelete = Button(frmQuestionEditor, text='Delete',command=self.DeleteQuestion,background = COLORS[2]
                                ,fg =COLORS[0],width=7,font=('Arial Rounded MT Bold',20),bd=0).place(x=585,y=590)
        #A frame created to hold the treeview table for all the questions
        self.tree_container = Frame(frmQuestionEditor,bg='white',bd=0,height=380,width=440)
        self.tree_container.place(x=50,y=160)
        #A frame which is used to view each questions and its details when selected
        self.label_container = Frame(frmQuestionEditor, bg='white', bd=0)
        self.label_container.place(x=520, y=160, width=420, height=367)
        self.questionsTable = ttk.Treeview(self.tree_container,columns=['Questions','Type','Difficulty'],show="headings",height=17)
        Columns = ['Questions','Type','Difficulty']
        self.questionsTable.column('Questions',width=275)
        self.questionsTable.column('Type',width=95)
        self.questionsTable.column('Difficulty',width=80)
        for c in Columns:
            self.questionsTable.heading(c, text=c,command = lambda column=c:self.SortTable(column,Columns.index(column)))
        if not New:
            self.AddQuestionstoTable()
        self.scroll = ttk.Scrollbar(self.tree_container,orient="vertical", command=self.questionsTable.yview)
        self.questionsTable.config(yscrollcommand=self.scroll.set)
        self.questionsTable.pack(side=LEFT,fill=Y,expand=True)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.questionLabel = Label(self.label_container,text='',bg='white',font=('Comic Sans MS',20),bd=0,wraplength=350)
        self.questionLabel.grid(row=0,column=0,sticky='nsew')
        self.answerLabel = Label(self.label_container,text='Double click question to show information',bg='white',wraplength=350
                                 ,font=('Comic Sans MS',20),bd=0)
        self.answerLabel.grid(row=1,column=0,stick='nsew')
        self.difficultyLabel = Label(self.label_container,text='',bg='white',font=('Comic Sans MS',20),bd=0)
        self.difficultyLabel.grid(row=2,column=0,sticky='nsew')
        self.label_container.columnconfigure(0, weight=1)
        self.label_container.rowconfigure(0,weight=1)
        self.label_container.rowconfigure(1,weight=1)
        self.label_container.rowconfigure(2,weight=1)
        self.IDs = self.questionsTable.get_children('')
        self.questionsTable.bind('<Double-Button-1>',self.SelectItem)
        self.questionsTable.bind_all('<MouseWheel>',self.MouseWheel)
        self.lblAverageDifficulty.config(text=self.GetAverageDifficulty(2))
        self.frmNew.bind('<Button-1>',self.ResetAnswer)
        self.entrSearch.bind('<Return>',self.SearchItem)

        #Method used to export all the questions in a set
        #to a csv file where the user can select the folder
        #and the name of the file to save it as which uses the
        #csv file
    def ExportQuestions(self):
        if self.questionsTable.get_children():
            try:
                FileName = filedialog.asksaveasfilename(filetypes=[('CSV Files', '*.csv')])
            except:
                messagebox.showerror("File Error", "Unable to access file")
            if FileName:
                with open(FileName, 'w', newline='', encoding='utf-8') as File:
                    writer = csv.writer(File)
                    writer.writerow(['Question', 'Type', 'Difficulty', 'Correct Answer', 'Incorrect Answers'])
                    for Question in self.Questions:
                        if Question[1] == 'Multiple Choice':
                            writer.writerow([Question[0], Question[1], Question[2], Question[3][0],(f"{Question[3][1][0]},{Question[3][2][0]},{Question[3][3][0]}")])
                        else:
                            writer.writerow([Question[0], Question[1], Question[2], Question[3],'-'])
                messagebox.showinfo('Export Successful', 'The questions have been exported successfully.')
                return
        else:
            messagebox.showinfo("No questions", "No questions found to export")

        #The Start method opens the Quiz window when the Start
        #button is pressed
    def Start(self):
        if self.questionsTable.get_children():
            self.SwitchWindow(Quiz,[self.UserID,self.CatID,self.Category[0],self.Questions])
        else:
            messagebox.showinfo("No questions", "No questions found to start")

        #The SearchItem method searches the table
        #for the data in the entry box in all of the
        #questions and updates the table if any values
        #are found in the table
    def SearchItem(self,event=None):
        for i in self.IDs:
            Found = False
            for x in self.questionsTable.item(i)['values']:
                if isinstance(x, str) and self.Search.get().lower() in x.lower():
                    Found = True
            if not Found:
                self.questionsTable.detach(i)
            else:
                self.questionsTable.reattach(i,'','end')

        #The GetAverageDifficulty method
        #calculates the average difficulty
        #of that set and returns a f string
        #with the average
    def GetAverageDifficulty(self,Index):
        Total = 0
        NumofItems = 0
        for x in self.questionsTable.get_children():
            Value = self.questionsTable.item(x)['values'][Index]
            Total += float(Value)
            NumofItems += 1
        Average = round(Total / NumofItems) if NumofItems != 0 else 0
        return f"Average Difficulty: {Average}/5"

        #The ResetAnswer method resets
        #the entry box when the user clicks
        #anywhere apart from the ClickableWidgets
    def ResetAnswer(self,event=None):
        ClickableWidgets = [self.questionsTable,self.btnStart,self.answerLabel,
                            self.questionLabel,self.difficultyLabel,self.entrSearch]
        if not(event.widget in ClickableWidgets):
            self.ResetAnswerLabel()
            self.Search.set('Search')

        #The SortTable method
        #sorts a column whenever the
        #header of that column is
        #pressed using the fnMergeSort function
        #and updating the table with the new values
    def SortTable(self,Column,Index):
        List = []
        for record in self.questionsTable.get_children(''):
            List.append((self.questionsTable.set(record,0),self.questionsTable.set(record,1),self.questionsTable.set(record,2)))
        List,self.Ordered = fnMergeSort(List,Index,self.Ordered,False)
        self.questionsTable.delete(*self.questionsTable.get_children())
        for x in List:
            self.questionsTable.insert('', 'end', values=x)

        #The ResetAnswerLabel method resets
        #the labels in the label_container
        #whenever the user clicks anywhere
        #else than the ClickableWidgets
        #in the ResetAnswer method
    def ResetAnswerLabel(self):
        self.answerLabel.config(text='Double click question to show information')
        self.difficultyLabel.config(text='')
        self.questionLabel.config(text='')

        #The EditQuestion method lets the user
        #to edit a selected question by opening the
        #QuestionAdder window with the selected question passed
        #but if no questions are selected then a messagebox showing an error
        #is shown 
    def EditQuestion(self):
        try:
            self.SelectedQuestion = self.questionsTable.selection()
            Question = self.questionsTable.item(self.SelectedQuestion)['values']
            if not Question:
                raise
        except:
             messagebox.showerror("Question error", "Select a question to edit")
             return
        newWindow = Toplevel(self.frmNew)
        self.top_level = QuestionAdder(newWindow,self.questionsTable,self.UserID,self.CatID,self.Questions,self.SelectedQuestion
                                           ,Question,True)

        #The DeleteQuestion method lets
        #the user to delete a question
        #that they have selected where
        #it's removed from the table and
        #from the database using the fnDeleteQuestion
        #function but if no question is selected then a
        #messagebox is shown
    def DeleteQuestion(self):
        try:
            self.SelectedQuestion = self.questionsTable.selection()
            Question = self.questionsTable.item(self.SelectedQuestion)['values']
            if not Question:
                raise
            getanswer = messagebox.askyesno('Delete Question','Are you sure you want to delete this question?')
            if getanswer > 0:
                if Question[1] == 'Multiple Choice':
                    fnDeleteIncorrectAnswers(Question[-1])
                fnDeleteQuestion(Question[-1])
                self.questionsTable.delete(self.SelectedQuestion)
                self.ResetAnswerLabel()
        except:
            messagebox.showerror("Question error", "Select a question to delete")
            return

        #The AddQuestionstoTable method
        #initially fills the table with
        #all the questions fetched from the
        #database using the fnFetchCategoryQuestions
        #function and also adding the questions
        #to self.Questions
    def AddQuestionstoTable(self):
        Empty = fnFetchCategoryQuestions(self.CatID)
        Questions = []
        for x in Empty:
            EmptyQuestion = []
            EmptyQuestion = [j for j in x]
            self.questionsTable.insert('', 'end', values=x)
            if x[1] == 'Multiple Choice':
                EmptyIncorrectAnswers = fnFetchIncorrectAnswers(x[-1])
                IncorrectAnswer = [i for i in EmptyIncorrectAnswers]
                EmptyQuestion[3] = list(EmptyQuestion[3]) + IncorrectAnswer
                connectedAnswer = ''.join(EmptyQuestion[3][:-3])
                IncorrectAnswers = [connectedAnswer] + EmptyQuestion[3][-3:]
                EmptyQuestion[3] = IncorrectAnswers
            Questions.append(EmptyQuestion)
        self.Questions = Questions

        #The MouseWheel method lets the
        #user to scroll through the table
        #when there are multiple questions
    def MouseWheel(self,event):
        self.questionsTable.yview_scroll(int(-1*(event.delta/120)),'units')

        #Changes the labels in the
        #label_container frame when
        #a question is double-clicked
        #and showing the question's details
    def SelectItem(self,event=None):
        try:
            self.SelectedQuestion = self.questionsTable.focus()
            Data = self.questionsTable.item(self.SelectedQuestion)['values']
            self.questionLabel.config(text=Data[0])
            self.answerLabel.config(text=Data[3])
            self.difficultyLabel.config(text=(Data[2],'/5'))
        except:
            return

        #Validation if the user has entered
        #a title for the new set of questions
        #which shows a messagebox if not
    def CheckSubject(self):
        try:
            if self.Subject.get() == 'Quiz Title' or self.Subject.get() == '':
                messagebox.showerror("showerror", "Enter a valid title")
                return False
            else:
                return True
        except:
            return True

        #The AddQuestion method runs when the New
        #button is pressed for the user to enter a
        #new question to the set of questions
    def AddQuestion(self):
        if self.New and not (self.Subject['state'] == 'readonly'):
            if self.SaveTitle():
                newWindow = Toplevel(self.frmNew)
                self.top_level = QuestionAdder(newWindow,self.questionsTable,self.UserID,self.CatID,self.Questions)
        else:
            newWindow = Toplevel(self.frmNew)
            self.top_level = QuestionAdder(newWindow,self.questionsTable,self.UserID,self.CatID,self.Questions)

        #The SaveTitle method saves the
        #title of the new set of questions
        #and adds it to the database with the
        #fnAddtotblUserCategory function
    def SaveTitle(self):
        if self.CheckSubject():
            getSave = messagebox.askyesno("Save Title", "Save quiz title?")
            if getSave > 0:
                self.Subject.config(state='readonly')
                self.CatID = fnAddQuizTitle(self.Subject.get())
                self.Category = fnFetchCategory(self.CatID)[0]
                fnAddtotblUserCategory(self.UserID, self.CatID)
                return True
            return False
        
#The QuestionAdder inherits from Window
#and allows the user to add a new
#question to the set of question 
class QuestionAdder(Window):
        #Initialize all the attributes
        #where the table, UserID,CatID and questions
        #are passed on as attributes
    def __init__(self,frmQuestionAdder,Treeview,UserID,CatID,Questions,SelectedQuestion=None,Question=None,Editing=None):
        Window.__init__(self,frmQuestionAdder,UserID,CatID)
        self.windowDimension(450,600)
        frmQuestionAdder.title("Question Adder")
        self.CanvasSetUp()
        frmQuestionAdder.bind('<Return>',self.SaveQuestion)
        self.Treeview = Treeview
        self.Question = Question
        #Editing holds a boolean value which indicates
        #if the user is editing if it's True
        #or adding a new question
        self.Editing = Editing
        self.Questions = Questions
        self.SelectedQuestion = SelectedQuestion
        self.intRadioChoice = IntVar()
        self.intRadioChoice.set(1)
        #The labels and entry boxes for holding the
        #details of the question
        self.lblQuestion = Label(frmQuestionAdder,text='Question:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblQuestion.place(x=15,y=10)
        self.entrQuestion = Text(frmQuestionAdder,width=29,height=4,font=('Calibri',20),fg=COLORS[1],bd=0)
        self.entrQuestion.place(x=17,y=49)
        self.lblType = Label(frmQuestionAdder,text='Type:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblType.place(x=15,y=190)
        #Four different radio buttons which
        #let the user to switch in between different
        #type of question as each type of question has
        #a different type of answer
        self.btnShortAnswer = Radiobutton(frmQuestionAdder,text='Short Answer',font=('Calibri',16),command=self.FrameSwitcher
                                          ,bg=COLORS[0],bd=0,value=1,variable=self.intRadioChoice,activebackground=COLORS[0])
        self.btnShortAnswer.place(x=100,y=225)
        self.btnNumerical = Radiobutton(frmQuestionAdder,text='Numerical',font=('Calibri',16),command=self.FrameSwitcher
                                        ,bg=COLORS[0],bd=0,value=2,variable=self.intRadioChoice,activebackground=COLORS[0])
        self.btnNumerical.place(x=270,y=225)
        self.btnMCQ = Radiobutton(frmQuestionAdder,text='Multiple Choice',font=('Calibri',16),command=self.FrameSwitcher
                                  ,bg=COLORS[0],bd=0,value=4,variable=self.intRadioChoice,activebackground=COLORS[0])
        self.btnMCQ.place(x=270,y=260)
        self.btnTrue_False = Radiobutton(frmQuestionAdder,text='True/False',font=('Calibri',16),command=self.FrameSwitcher
                                         ,bg=COLORS[0],bd=0,value=3,variable=self.intRadioChoice,activebackground=COLORS[0])
        self.btnTrue_False.place(x=100,y=260)
        self.lblRating = Label(frmQuestionAdder,text='Rating:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblRating.place(x=15,rely=0.87)
        self.rating = Spinbox(frmQuestionAdder,from_=1, to=5,font=('Calibri',22),fg=COLORS[1],width=10,bd=0,state='readonly')
        self.rating.place(relx=0.47,rely=0.91,anchor='center')
        self.btnSave = Button(frmQuestionAdder,text='Save',background = COLORS[2],command=self.SaveQuestion,fg =COLORS[0]
                              ,font=('Arial Rounded MT Bold',20),bd=0)
        self.btnSave.place(relx=0.75,rely=0.87)
        #Frame created to hold the answer for a
        #short term or numerical question
        self.frmAnswer = Frame(frmQuestionAdder,bg=COLORS[0],bd=0,height=200,width=410)
        self.lblAnswer = Label(self.frmAnswer,text='Answer:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblAnswer.place(x=0,rely=0.75)
        self.entrAnswer = Entry(self.frmAnswer,fg=COLORS[1],bd=0,font=('Calibri',20))
        self.entrAnswer.place(x=112,rely=0.775,width=400)
        #Frame created for holding the answer 
        #for a True or False question
        self.frmTrueFalse = Frame(frmQuestionAdder,bg=COLORS[0],bd=0,height=200,width=410)
        self.lblTFAnswer = Label(self.frmTrueFalse,text='Answer:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblTFAnswer.place(x=0,rely=0.75)
        self.comboTF = ttk.Combobox(self.frmTrueFalse,values=['True','False'],width=30,state='readonly')
        self.comboTF.set('True')
        self.comboTF.place(x=112,rely=0.775,height=35)
        #Frame created for holding the answer
        #to a multiple choice question with
        #the incorrect answers as well
        self.frmMCQ = Frame(frmQuestionAdder,bg=COLORS[0],bd=0,height=200,width=410)
        self.lblMCQAnswer = Label(self.frmMCQ,text='Answer:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
        self.lblMCQAnswer.grid(row=0,column=0)
        self.entrMCQAnswer = Entry(self.frmMCQ,fg=COLORS[1],bd=0,font=('Calibri',20))
        self.entrMCQAnswer.grid(row=0,column=1,sticky='w')
        self.entrMCQFalse1 = Entry(self.frmMCQ,fg=COLORS[1],bd=0,font=('Calibri',20))
        self.entrMCQFalse1.grid(row=1,column=1,sticky='w')
        self.entrMCQFalse2 = Entry(self.frmMCQ,fg=COLORS[1],bd=0,font=('Calibri',20))
        self.entrMCQFalse2.grid(row=2,column=1,sticky='w')
        self.entrMCQFalse3 = Entry(self.frmMCQ,fg=COLORS[1],bd=0,font=('Calibri',20))
        self.entrMCQFalse3.grid(row=3,column=1,sticky='w')
        for i in range(3):
            self.lblWrong = Label(self.frmMCQ,text='Wrong:',bg=COLORS[0],fg=COLORS[1],font=('Georgia',22))
            self.lblWrong.grid(row=i+1,column=0)
        self.frmMCQ.columnconfigure(0, weight=1)
        self.frmMCQ.columnconfigure(1, weight=1)
        self.frmMCQ.rowconfigure(0,weight=1)
        self.frmMCQ.rowconfigure(1,weight=1)
        self.frmMCQ.rowconfigure(2,weight=1)
        self.frmMCQ.rowconfigure(3,weight=1)
        self.CurrentFrame = self.frmAnswer
        self.CurrentFrame.place(x=15,y=310)
        #Runs the EditingQuestion method
        #if the user is currently
        #editing the question
        if self.Editing:
            self.EditingQuestion()
        frmQuestionAdder.grab_set()

        #The SaveQuestion method validates 
        #the question using the ValidateQuestion
        #method and formatting it 
        #afterwards, the table is 
        #then updated by adding the 
        #question to it and then updating
        #the database with the functions
        #fnAddtotblIncorrectAnswers, fnAddtotblQuestions
    def SaveQuestion(self, event=None):
        if self.Editing:
            if self.ValidateQuestion():
                Question = self.FormatQuestion()
                Question[-1] = self.Question[-1]
                self.Treeview.item(self.SelectedQuestion,values=Question)
                for x in self.Questions:
                    if x[-1] == Question[-1]:
                        self.Questions[self.Questions.index(x)] = Question
                if Question[1] == 'Multiple Choice':                            
                    IncAns = Question[3][1:4]                                       
                    Question[3] = Question[3][0]
                    fnUpdateQuestion(Question)
                    fnDeleteIncorrectAnswers(self.Question[-1])
                    for x in IncAns:
                        IncAnsID = fnAddtotblIncorrectAnswers(Question[-1],x)
                        fnAddtotblQuestionIncorrectAnswer(IncAnsID,Question[-1])
                else:
                    fnUpdateQuestion(Question)
                self.CloseWindow(True)
        else:
            if self.ValidateQuestion():
                Question = self.FormatQuestion()
                if Question[1] == 'Multiple Choice':
                    if any(Question[3].count(x) >  1 for x in Question[3]):
                        messagebox.showerror('Question Error','Repeated answer found')
                        return
                    self.Questions=Question
                    IncAns = Question[3][1:4]
                    Question[3] = Question[3][0]
                    QuestionID = fnAddtotblQuestions(Question)
                    for x in IncAns:
                        IncAnsID = fnAddtotblIncorrectAnswers(QuestionID,x)
                        fnAddtotblQuestionIncorrectAnswer(IncAnsID,QuestionID)
                else:
                    self.Questions.append(Question)
                    fnAddtotblQuestions(Question)
                self.Treeview.insert('', 'end', values=Question)
                self.CloseWindow(True)

        #The EditingQuestion method
        #adds the details of the 
        #selected question passed to the
        #entry boxes and the other widgets
    def EditingQuestion(self):
        self.CurrentFrame.place_forget()
        Question = StringVar(value=self.Question[0])
        self.entrQuestion.insert("1.0", Question.get())
        Rating = IntVar(value=self.Question[2])
        self.rating.config(textvariable=Rating)
        if self.Question[1] == 'Multiple Choice' :
            self.CurrentFrame = self.frmMCQ
            IncorrectAnswers = fnFetchIncorrectAnswers(self.Question[-1])
            Answer = StringVar(value=self.Question[3])
            self.entrMCQAnswer.config(textvariable=Answer)
            False1 = StringVar(value=(''.join(IncorrectAnswers[0])))
            self.entrMCQFalse1.config(textvariable=False1)
            False2 = StringVar(value=(''.join(IncorrectAnswers[1])))
            self.entrMCQFalse2.config(textvariable=False2)
            False3 = StringVar(value=(''.join(IncorrectAnswers[2])))
            self.entrMCQFalse3.config(textvariable=False3)
            self.intRadioChoice.set(4)
            self.btnShortAnswer.configure(state=DISABLED)
            self.btnTrue_False.configure(state=DISABLED)
            self.btnNumerical.configure(state=DISABLED)
        elif self.Question[1] == 'Short Answer' or self.Question[1] == 'Numerical':
            self.CurrentFrame = self.frmAnswer
            Answer = StringVar(value=self.Question[3])
            self.entrAnswer.config(textvariable=Answer)
            self.btnMCQ.configure(state=DISABLED)
            self.btnTrue_False.configure(state=DISABLED)
            if self.Question[1] == 'Short Answer':
                self.intRadioChoice.set(1)
                self.btnNumerical.configure(state=DISABLED)
            else:
                self.intRadioChoice.set(2)
                self.btnShortAnswer.configure(state=DISABLED)
        else:
            self.CurrentFrame = self.frmTrueFalse
            Answer = StringVar(value=self.Question[3])
            self.comboTF.set(self.Question[3])
            self.intRadioChoice.set(3)
            self.btnShortAnswer.configure(state=DISABLED)
            self.btnMCQ.configure(state=DISABLED)
            self.btnNumerical.configure(state=DISABLED)
        self.CurrentFrame.place(x=15,y=310)

        #The FormatQuestion method formats
        #the question in the require form which is
        #Question,Question Type,Difficulty,Answer 
        #and Category ID and then returns the updated question
    def FormatQuestion(self):
        Question = []
        Question.append(self.entrQuestion.get("1.0", "end-1c"))
        if self.intRadioChoice.get() == 4:
            Question.append(self.btnMCQ['text'])
            Question.append(self.rating.get())
            Answers = []
            Answers.append(self.entrMCQAnswer.get())
            Answers.append(self.entrMCQFalse1.get())
            Answers.append(self.entrMCQFalse2.get())
            Answers.append(self.entrMCQFalse3.get())     
            Question.append(Answers)
        elif self.intRadioChoice.get() == 3:
            Question.append(self.btnTrue_False['text'])
            Question.append(self.rating.get())
            Question.append(self.comboTF.get())
        elif self.intRadioChoice.get() == 1:
            Question.append(self.btnShortAnswer['text'])
            Question.append(self.rating.get())
            Question.append(self.entrAnswer.get())
        else:
            Question.append(self.btnNumerical['text'])
            Question.append(self.rating.get())
            Question.append(self.entrAnswer.get())
        Question.append(self.CatID)
        return Question
        
        #Validates the question and its answer
        #such as checking if a numerical
        #answer is entered for a numerical question
    def ValidateQuestion(self):
        if self.entrQuestion.get("1.0", "end-1c") == '':
            messagebox.showinfo("Question Error", "Enter a question")
            return False
        elif self.intRadioChoice.get() == 1 and self.entrAnswer.get() == '':
            messagebox.showinfo("Answer Error", "Enter an answer")
            return False
        elif self.intRadioChoice.get() == 2:
            try:
                int(self.entrAnswer.get())
            except:
                try:
                    float(self.entrAnswer.get())
                except:
                    messagebox.showinfo("Answer Error", "Enter a valid numerical answer")
                    return False
        elif self.intRadioChoice.get() == 4 and not(self.entrMCQAnswer.get() and self.entrMCQFalse1.get() and self.entrMCQFalse2.get()
                                                    and self.entrMCQFalse3.get()):
            messagebox.showinfo("Answer Error", "Enter an answer")
            return False
        return True
        
        #Switches the current frame to other frames
        #based on the intRadioChoice which is
        #the current radio button selected
    def FrameSwitcher(self):
        if self.intRadioChoice.get() == 2 or self.intRadioChoice.get() == 1:
            self.CurrentFrame.place_forget()
            self.CurrentFrame = self.frmAnswer
            self.CurrentFrame.place(x=15,y=310)
        elif self.intRadioChoice.get() == 4:
            self.CurrentFrame.place_forget()
            self.CurrentFrame = self.frmMCQ
            self.CurrentFrame.place(x=15,y=310)
        else:
            self.CurrentFrame.place_forget()
            self.CurrentFrame = self.frmTrueFalse
            self.CurrentFrame.place(x=15,y=310)

        #Closes the window and returns to the
        #QuestionAdder window where the question
        #is added to the table
    def CloseWindow(self,Save=None):
        if Save == None:
            getExit = messagebox.askyesno(title="Quit",message="Are you sure you want to quit?")
            if not getExit:
                return
        self.frmNew.grab_release()
        self.frmNew.destroy()

#The Quiz inherits from Window
#where the user can answer the questions
#of that set of questions
class Quiz(Window):
    def __init__(self,frmQuiz,UserID,CatID,Category,Questions):
        Window.__init__(self,frmQuiz,UserID,CatID)
        self.windowDimension(1000,700)
        frmQuiz.title("Quiz")
        self.CanvasSetUp()
        self.Category = Category
        #Shuffles Questions using the
        #random module
        random.shuffle(Questions)
        self.Questions = Questions
        self.Answers = []
        self.QuestionPosition = None
        self.CurrentQuestionIndex = 0
        self.Question = self.Questions[self.CurrentQuestionIndex]
        self.btnRadioChoice = IntVar()
        self.btnRadioChoice.set(-1)
        self.QuestionHold = StringVar()
        self.Title = Label(frmQuiz,text=self.Category,bg = COLORS[0],fg =COLORS[1],font=('Forte',40,'underline'))
        self.Title.place(x=50,y=20,anchor='nw')
        self.Difficulty = Label(frmQuiz,justify=LEFT,bg = COLORS[0],fg =COLORS[1],font=('Berlin Sans fb demi',25))
        self.Difficulty.place(x=50,y=210)
        self.btnQuit = Button(frmQuiz,text='Quit',width=7,bg = COLORS[1],command=self.QuitQuiz,fg =COLORS[0]
                              ,font=('Berlin Sans fb demi',25),bd=0)
        self.btnQuit.place(x=801,y=25)
        self.QuestionsLeft = Label(frmQuiz,text='Progress:',bg = COLORS[0],fg =COLORS[1],font=('Berlin Sans fb demi',30))
        self.QuestionsLeft.place(x=130,y=120)
        self.btnNext = Button(frmQuiz,text='Next',background = COLORS[2],command=self.NextButton,fg =COLORS[0],width=8
                              ,font=('Arial Rounded MT Bold',25),bd=0)
        self.btnNext.place(x=500,y=650,anchor='s')
        self.btnFinish = Button(frmQuiz,text='Finish',background = COLORS[2],command =self.FinishButton,fg =COLORS[0],width=8
                                ,font=('Arial Rounded MT Bold',25),bd=0)
        #The progress bar shows the position and how many questions
        #they have answered as an infographic where it visualizes the position
        self.ProgressBar = ttk.Progressbar(frmQuiz,orient="horizontal", length=400, mode="determinate",max=len(self.Questions))
        self.ProgressBar.place(x=500,y=150,anchor='center')
        self.QuestionPlace = Label(frmQuiz,bg = COLORS[0],fg =COLORS[1],font=('Berlin Sans fb demi',30))
        self.QuestionPlace.place(x=720,y=120)
        self.Line = self.BackCanvas.create_line(50,200,940,200, fill="#2E2928", width=5)
        #Frame created to hold the label for the question
        self.frmQuestion = Frame(frmQuiz,bg=COLORS[0],height=100,width=600)
        self.frmQuestion.place(x=200,y=230)
        self.lblQuestion = Label(self.frmQuestion,textvariable=self.QuestionHold,bg = COLORS[0],fg =COLORS[1],font=('Berlin Sans fb demi',30))
        self.lblQuestion.place(relx=0.5,rely=0.5,anchor='center')
        #Frame created to hold the label and entry for the answer
        self.frmAnswer = Frame(frmQuiz,bg=COLORS[0],height=230,width=600)
        self.entrAnswer = Entry(self.frmAnswer,fg=COLORS[1],bd=0,font=('Calibri',20),width=20)
        self.entrAnswer.place(rely=0.5,relx=0.6,anchor='center')
        self.lblAnswer = Label(self.frmAnswer,text='Answer: ',bg = COLORS[0],fg =COLORS[1],font=('Berlin Sans fb demi',30))
        self.lblAnswer.place(rely=0.5,relx=0.1,anchor='w')
        #Frame created for a multiple choice question
        self.frmMCQAnswer = Frame(frmQuiz,bg=COLORS[0],height=230,width=600)
        self.lblMCQAnswer = Label(self.frmMCQAnswer,text='Answer: ',bg = COLORS[0],fg =COLORS[1],font=('Berlin Sans fb demi',30))
        self.lblMCQAnswer.place(x=0,y=0)
        self.btnAnswer1 = Radiobutton(self.frmMCQAnswer,value=1,variable=self.btnRadioChoice
                                      ,font=('Calibri',20),bg=COLORS[0],bd=0,activebackground=COLORS[0]) #,variable=self.intRadioChoice
        self.btnAnswer1.place(anchor='w',y=100,x=40)
        self.btnAnswer2 = Radiobutton(self.frmMCQAnswer,value=2,variable=self.btnRadioChoice
                                      ,font=('Calibri',20),bg=COLORS[0],bd=0,activebackground=COLORS[0]) #,variable=self.intRadioChoice
        self.btnAnswer2.place(anchor='w',y=170,x=40)
        self.btnAnswer3 = Radiobutton(self.frmMCQAnswer,value=3,variable=self.btnRadioChoice
                                      ,font=('Calibri',20),bg=COLORS[0],bd=0,activebackground=COLORS[0]) #,variable=self.intRadioChoice
        self.btnAnswer3.place(anchor='w',y=170,x=390)
        self.btnAnswer4 = Radiobutton(self.frmMCQAnswer,value=4,variable=self.btnRadioChoice
                                      ,font=('Calibri',20),bg=COLORS[0],bd=0,activebackground=COLORS[0]) #,variable=self.intRadioChoice
        self.btnAnswer4.place(anchor='w',y=100,x=390)
        #Frame created for holding the answer to a True or False question
        self.frmTrue_False = Frame(frmQuiz,bg=COLORS[0],height=230,width=600)
        self.comboTFAnswer = ttk.Combobox(self.frmTrue_False,values=['True','False'],width=20,state='readonly',font=('Calibri',20))
        self.comboTFAnswer.set('True')
        self.lblTFAnswer = Label(self.frmTrue_False,text='Answer: ',bg = COLORS[0],fg =COLORS[1],font=('Berlin Sans fb demi',30))
        self.lblTFAnswer.place(rely=0.5,relx=0.1,anchor='w')
        self.comboTFAnswer.place(rely=0.5,relx=0.63,anchor='center')
        self.CurrentFrame = self.frmAnswer
        self.IndexQuestions()
        self.SwitchFrames(self.Questions[self.CurrentQuestionIndex])
        frmQuiz.bind('<Return>',self.NextButton)
        
        #Indexes the questions to show the
        #position and which question a user
        #is on when answering the questions
    def IndexQuestions(self):
        for i in range(len(self.Questions)):
            self.Questions[i].insert(0,i + 1)

        #The NextButton method moves to the
        #next question by updating the frames
        #if the answer is validated 
    def NextButton(self,event=None):
        if self.ValidateAnswer(self.Questions[self.CurrentQuestionIndex]):
            self.GetAnswer(self.Questions[self.CurrentQuestionIndex])
            self.CurrentQuestionIndex += 1
            self.ResetEntries()
            self.SwitchFrames(self.Questions[self.CurrentQuestionIndex])
            if (self.CurrentQuestionIndex + 1) == len(self.Questions):
                self.btnNext.destroy()
                self.btnFinish.place(x=500,y=650,anchor='s')
                self.frmNew.bind('<Return>',self.FinishButton)
                return

        #The QuuitQuiz method is runned when the Quit
        #button is pressed where the user quits the quiz
        #and returns to the QuestionEditor window
    def QuitQuiz(self):
        getAnswer = messagebox.askyesno("Quit?", "Are you sure you want to quit?")
        if getAnswer > 0:
            Category = fnFetchCategory(self.CatID)
            self.SwitchWindow(QuestionsEditor,[False,self.UserID,Category[0],self.CatID])
            
        #The FinishButton method is ran
        #when the Finish button is pressed
        #which switches to the Results window
    def FinishButton(self,event=None):
        self.GetAnswer(self.Questions[self.CurrentQuestionIndex])
        self.SwitchWindow(Results,[self.UserID,self.CatID,self.Answers,self.Questions,self.Category])
        
        #Adds the answer for each question to
        #Answers 
    def GetAnswer(self,Question):
        if Question[2] == 'Short Answer' or Question[2] == 'Numerical':
            self.Answers.append(self.entrAnswer.get())
        elif Question[2] == 'Multiple Choice':
            Choice = self.btnRadioChoice.get()
            if Choice == 1:
                self.Answers.append(self.btnAnswer1.cget('text'))
            elif Choice == 2:
                self.Answers.append(self.btnAnswer2.cget('text'))
            elif Choice == 3:
                self.Answers.append(self.btnAnswer3.cget('text'))
            else:
                self.Answers.append(self.btnAnswer4.cget('text'))
        else:
            self.Answers.append(self.comboTFAnswer.get())

        #Resets all the entries as
        #they hold the answer of the
        #previous question
    def ResetEntries(self):
        self.btnRadioChoice.set(-1)
        self.entrAnswer.delete(0, 'end')
        self.comboTFAnswer.set('True')

        #The ValidateAnswer method
        #validates the answer they entered
        #and shows a messagebox is not validated
        #returning False
    def ValidateAnswer(self,Question):
        if Question[2] == 'Short Answer' and self.entrAnswer.get() == '':
            messagebox.showinfo("Answer Error", "Enter an answer")
            return False
        elif Question[2] == 'Numerical':
            try:
                int(self.entrAnswer.get())
            except:
                try:
                    float(self.entrAnswer.get())
                except:
                    messagebox.showinfo("Answer Error", "Enter a valid numerical answer")
                    return False
        elif Question[2] == 'Multiple Choice' and self.btnRadioChoice.get() == -1:
            messagebox.showinfo("Answer Error", "Choose an option")
            return False
        return True

        #The SwitchFrames method
        #switches frames depending on
        #what type of question is up
        #while also changing the
        #progress bar adn the index
    def SwitchFrames(self,Question):
        self.QuestionPlace.config(text=(Question[0],'/',len(self.Questions)))
        self.ProgressBar["value"] = Question[0]
        self.QuestionHold.set(f"Q{Question[0]}. {Question[1]}")
        self.Difficulty.config(text=(f"Difficulty:\n{Question[3]}/5"))
        if Question[2] == 'Short Answer' or Question[2] == 'Numerical':
            self.CurrentFrame.place_forget()
            self.CurrentFrame = self.frmAnswer
            self.CurrentFrame.place(x=200,y=320)
        elif Question[2] == 'Multiple Choice':
            random.shuffle(Question[4])
            self.CurrentFrame.place_forget()
            self.CurrentFrame = self.frmMCQAnswer
            self.CurrentFrame.place(x=200,y=320)
            self.btnAnswer1.config(text=Question[4][0][0] if isinstance(Question[4][0], tuple) else str(Question[4][0]))
            self.btnAnswer2.config(text=Question[4][1][0] if isinstance(Question[4][1], tuple) else str(Question[4][1]))
            self.btnAnswer3.config(text=Question[4][2][0] if isinstance(Question[4][2], tuple) else str(Question[4][2]))
            self.btnAnswer4.config(text=Question[4][3][0] if isinstance(Question[4][3], tuple) else str(Question[4][3]))
        else:
            self.CurrentFrame.place_forget()
            self.CurrentFrame = self.frmTrue_False
            self.CurrentFrame.place(x=200,y=320)

#The Results class inherits from Window
#that displays the user the results of their
#answers and their score on it
class Results(Window):
    def __init__(self,frmResults,UserID,CatID,Answers,Questions,Category):
        Window.__init__(self,frmResults,UserID,CatID)
        self.windowDimension(1000,700)
        frmResults.title("Results")
        self.CanvasSetUp()
        self.Answers = Answers 
        self.Questions = Questions
        self.Category = Category
        self.Correct = 0
        self.Score = 0
        self.Line = self.BackCanvas.create_line(50,130,940,130, fill="#2E2928", width=5)
        self.lblScore = Label(frmResults,bg=COLORS[0],fg=COLORS[1],font=('Berlin Sans fb demi',30))
        self.lblScore.place(x=50,y=50)
        self.ProgressBar = ttk.Progressbar(frmResults,orient="horizontal", length=400, mode="determinate",max=len(self.Answers))
        self.ProgressBar.place(relx=0.5,y=70,anchor='center')
        self.lblResults = Label(frmResults,bg=COLORS[0],fg=COLORS[1],justify=LEFT,font=('Berlin Sans fb demi',30))
        self.lblResults.place(x=770,y=30)
        self.frmResults = Frame(frmResults,bg='white',bd=0,height=420,width=890)
        self.frmResults.place(x=50,y=160)
        self.btnRetry = Button(frmResults,text='Retry',command=self.Retry,width=7,bg = COLORS[1],fg =COLORS[0],font=('Berlin Sans fb demi',25),bd=0)
        self.btnSave = Button(frmResults,text='Save',command=self.SaveResults,width=7,bg = COLORS[1],fg =COLORS[0],font=('Berlin Sans fb demi',25),bd=0)
        self.btnRetry.place(y=650,relx=0.3,anchor=E)
        self.btnSave.place(y=650,relx=0.7,anchor=W)
        self.BackArrow = PhotoImage(file='Back-Arrow.gif')
        self.btnBack = Button(frmResults,image=self.BackArrow,command=self.Return,borderwidth=0,highlightthickness=0)
        self.btnBack.place(x=8,y=4)
        self.ResultsTable = ttk.Treeview(self.frmResults,columns=['Question','Question Type','Correct Answer','Answer'],show="headings",height=20)
        self.ResultsTable.column('Question',width=240)
        self.ResultsTable.column('Answer',width=240)
        self.ResultsTable.column('Correct Answer',width=240)
        self.ResultsTable.column('Question Type',width=150)
        self.Scroll = ttk.Scrollbar(self.frmResults,orient="vertical", command=self.ResultsTable.yview)
        self.ResultsTable.config(yscrollcommand=self.Scroll.set)
        self.Scroll.pack(side=RIGHT, fill=Y)
        self.ResultsTable.pack(fill='both',expand=True)
        self.ResultsTable.heading('Question', text='Question')
        self.ResultsTable.heading('Answer', text='Answer')
        self.ResultsTable.heading('Correct Answer', text='Correct Answer')
        self.ResultsTable.heading('Question Type', text='Question Type')
        self.Style = ttk.Style()
        self.Style.configure("Treeview")
        self.Style.map("Treeview", background=[("selected", "grey")])
        self.ResultsTable.tag_configure("red", background="red")
        self.ResultsTable.tag_configure("green", background="green", foreground="black")
        self.AddToTable()

        #The CheckAnswer method checks the answer with the correct answer
        #by either checking if they exactly match or is the correct answer
        #is in the answer or comparing the Jaccard Coefficient
        #with the minimum threshold of 0.5 and returning True
    def CheckAnswer(self,CorrectAnswer,UserAnswer):
        if UserAnswer.strip().lower() == CorrectAnswer.lower():
            return True
        elif CorrectAnswer.lower() in UserAnswer.strip().lower():
            return True
        UserSet = set(UserAnswer.lower().split())
        CorrectSet = set(CorrectAnswer.lower().split())
        JaccardCoefficient = GetJaccardCoefficient(UserSet,CorrectSet)
        if JaccardCoefficient >= 0.5:
            return True
        return False

        #Adds the questions and the answers provided to the
        #table and colors them green or red whether they got
        #right or wrong 
    def AddToTable(self):
        for i in range(len(self.Answers)):
            if self.Questions[i][2] == 'Multiple Choice':
                for x in self.Questions[i][4]:
                    if isinstance(x,str):
                        item = self.ResultsTable.insert('','end',values=(self.Questions[i][1],self.Questions[i][2],x,self.Answers[i]))
                        if self.CheckAnswer(x,self.Answers[i]):
                            self.ResultsTable.item(item, tags=("green",))
                            self.Correct += 1
                        else:
                            self.ResultsTable.item(item, tags=("red",))
            else:
                item = self.ResultsTable.insert('','end',values=(self.Questions[i][1],self.Questions[i][2],self.Questions[i][4],self.Answers[i]))
                if self.CheckAnswer(self.Questions[i][4],self.Answers[i]):
                    self.ResultsTable.item(item, tags=("green",))
                    self.Correct += 1
                else:
                    self.ResultsTable.item(item, tags=("red",))   
        self.CalculateResults()

        #The CalculateResults method calculates the score
        #and marks of the set and updates the labels
    def CalculateResults(self):
        self.Score = round((self.Correct / len(self.Answers)) * 100) if len(self.Answers) != 0 else 0
        self.lblScore.config(text=(f"Score: {self.Score}%"))
        Length = len(self.Answers)
        self.lblResults.config(text=(f"Marks:\n{self.Correct}/{Length}"))
        self.ProgressBar["value"] = self.Correct

        #Returns to the QuestionEditor window
        #but asking whether to save results
        #before returning with a messagebox
    def Return(self):
        getExit = messagebox.askyesno(title="Return",message="Save results?")
        if getExit > 0:
            self.SaveResults()
        else:
            self.SwitchWindow(QuestionsEditor,[False,self.UserID,self.Category,self.CatID])
        return

        #The SaveResults method updates
        #the score for the set using the
        #fnUpdateScore function and also switching
        #to the QuestionEditor window
    def SaveResults(self):
        fnUpdateScore(self.CatID,self.Score)
        Category = fnFetchCategory(self.CatID)
        self.SwitchWindow(QuestionsEditor,[False,self.UserID,Category[0],self.CatID])

        #The Retry method allows the user
        #to retry the set of questions
        #by switching to the Quiz window
    def Retry(self):
        for i in range(len(self.Questions)):
            self.Questions[i].pop(0)
        self.SwitchWindow(Quiz,[self.UserID,self.CatID,self.Category,self.Questions])
        



    #The GetJaccardCoefficient function
    #calculates the Jaccard coefficient
    #by dividing the intersection of the two sets
    #with the union
def GetJaccardCoefficient(set1,set2):
    Intersection = len(set1.intersection(set2))
    Union = len(set1.union(set2))
    return Intersection / Union if Union != 0 else 0

    #The fnGetHashValue creates a hash value
    #for the key provided using the hashlib module
def fnGetHashValue(key):                
    key = key.encode()
    hash_value = hashlib.blake2s(key).hexdigest()
    return hash_value

    #The fnMergeSort function performs a merge sort
    #both in ascending and descending order
    #on a list provided where it also uses recursion
def fnMergeSort(List,Index,Ordered=False,Reverse=False):
    if len(List) > 1:
        mid = len(List) // 2
        leftList = List[:mid]
        rightList = List[mid:]
        fnMergeSort(leftList,Index,Ordered,Reverse)
        fnMergeSort(rightList,Index,Ordered,Reverse)
        i = 0
        j = 0
        k = 0
        while i < len(leftList) and j < len(rightList):
            if (not Reverse and leftList[i][Index] < rightList[j][Index]) or (Reverse and leftList[i][Index] > rightList[j][Index]):
                List[k] = leftList[i]
                i += 1
            else:
                List[k] = rightList[j]
                j += 1
            k += 1
        while i < len(leftList) :
            List[k] = leftList[i]
            i += 1
            k += 1
        while j < len(rightList):
            List[k] = rightList[j]
            j += 1
            k += 1
        if not Ordered:
            return List, True
        else:
            return List[::-1], False
    
    #The fnCreateDatabase function
    #runs a sql statement to create the
    #the database and the tables in the
    #database
def fnCreateDatabase(c):
    c.executescript('''
        CREATE TABLE IF NOT EXISTS tblQuestions
        (QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
        Question varchar (200) NOT NULL,
        Answer varchar (200) NOT NULL,
        Question_Type varchar (200) NOT NULL,
        Rating INTEGER NOT NULL,
        CatID INT NOT NULL,
        FOREIGN KEY (CatID) REFERENCES tblCategory (CatID));

        CREATE TABLE IF NOT EXISTS tblUsers
        (UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username varchar(50) NOT NULL,
        Password varchar (50) NOT NULL,
        E_Mail varchar (100) NOT NULL,
        Firstname varchar (50) NOT NULL,
        Secondname varchar (50) NOT NULL,
        Age INTEGER NOT NULL);

        CREATE TABLE IF NOT EXISTS tblIncorrectAnswers
        (IncAnsID INTEGER PRIMARY KEY AUTOINCREMENT,
        Incorrect_Answer varchar (100) NOT NULL);

        CREATE TABLE IF NOT EXISTS tblCategory
        (CatID INTEGER PRIMARY KEY AUTOINCREMENT,
        Category varchar (200) NOT NULL,
        Recent_Score INT);

        CREATE TABLE IF NOT EXISTS tblQuestionIncorrectAnswers
        (IncAnsID INT NOT NULL PRIMARY KEY,
        QuestionID INT NOT NULL,
        FOREIGN KEY (IncAnsID) REFERENCES tblIncorrectAnswers(IncAnsID),
        FOREIGN KEY (QuestionID) REFERENCES tblQuestions(QuestionID));
        
        CREATE TABLE IF NOT EXISTS tblUserCategory
        (CatID INTEGER NOT NULL PRIMARY KEY,
        UserID INTEGER NOT NULL,
        FOREIGN KEY (UserID) REFERENCES tblUsers (UserID),
        FOREIGN KEY (CatID) REFERENCES tblCategory (CatID)); 
        ''')
    connection.commit()

    #The fnFetchAllUsers function
    #fetches all the users' details from the
    #database
def fnFetchAllUsers():
    cursor.execute(
        "SELECT * FROM tblUsers")
    return cursor.fetchall()

    #The fnAddtotblUsers function
    #adds user details to the database
def fnAddtotblUsers(Data):
    cursor.execute(
        "INSERT INTO tblUsers(Username,Password,E_Mail,Firstname,Secondname,Age) \
            VALUES (?,?,?,?,?,?)",Data)
    connection.commit()
    return cursor.lastrowid

    #The fnAddtotblQuestions function
    #adds a question to the database
def fnAddtotblQuestions(Question):
    cursor.execute(
        'INSERT INTO tblQuestions(Question, Answer, Question_Type, Rating, CatID) \
            VALUES (?,?,?,?,?)',(Question[0],Question[3],Question[1],Question[2],Question[4]))
    connection.commit()
    return cursor.lastrowid

    #The fnAddQuizTitle function
    #adds the category title to the
    #database
def fnAddQuizTitle(Category):
    cursor.execute(
        'INSERT INTO tblCategory(Category) \
            VALUES (?);',[Category])
    connection.commit()
    return cursor.lastrowid

    #The fnAddtotblUserCategory function
    #adds the user id and cat id to the
    #table tblUserCategory
def fnAddtotblUserCategory(UserID, CatID):
    cursor.execute(
        'INSERT INTO tblUserCategory(UserID, CatID) \
            VALUES(?,?)',(UserID,CatID))
    connection.commit()
    return cursor.lastrowid

    #The fnAddtotblIncorrectAnswers function
    #adds incorrect answers to the tblIncorrectAnswers
    #table and autoincrements the ID
def fnAddtotblIncorrectAnswers(QuestionID,IncAns):
    cursor.execute(
        'INSERT INTO tblIncorrectAnswers(Incorrect_Answer) \
            VALUES(?)',[IncAns])
    connection.commit()
    return cursor.lastrowid
    
    #The fnAddtotblQuestionIncorrectAnswer function
    #adds the IncAnsID and the QuestionID to the 
    #tblQuestionIncorrectAnswers table
def fnAddtotblQuestionIncorrectAnswer(IncAnsID,QuestionID):
    cursor.execute(
        'INSERT INTO tblQuestionIncorrectAnswers(IncAnsID,QuestionID)\
            VALUES(?,?)',(IncAnsID,QuestionID))
    connection.commit()
    

    #The fnFetchCategoriesUsers function
    #fetches all the sets for that user
def fnFetchCategoriesUsers(UserID):
    cursor.execute(
        'SELECT tblCategory.Category, tblCategory.Recent_Score, tblCategory.CatID FROM tblCategory \
        INNER JOIN tblUserCategory ON tblUserCategory.CatID = tblCategory.CatID \
        WHERE tblUserCategory.UserID = ?',[UserID])
    return cursor.fetchall()

    #The fnFetchCategoryQuestions function
    #fetches all the questions for the category
def fnFetchCategoryQuestions(CatID):
    cursor.execute(
        'SELECT tblQuestions.Question,tblQuestions.Question_Type,tblQuestions.Rating,tblQuestions.Answer,tblQuestions.QuestionID \
        FROM tblQuestions \
        INNER JOIN tblCategory ON tblCategory.CatID = tblQuestions.CatID \
        WHERE tblQuestions.CatID = ?',[CatID])
    return cursor.fetchall()

    #The fnFetchIncorrectAnswers function
    #fetches the incorrect answers for that
    #question
def fnFetchIncorrectAnswers(QuestionID):
    cursor.execute(
        'SELECT Incorrect_Answer \
        FROM tblIncorrectAnswers \
        WHERE IncAnsID IN (SELECT IncAnsID FROM tblQuestionIncorrectAnswers WHERE QuestionID = ?)',[QuestionID])
    return cursor.fetchall()

    #The fnUpdateQuestion function
    #updates the values for that question
def fnUpdateQuestion(Question):
    cursor.execute(
        'UPDATE tblQuestions \
        SET Question = ?, Question_Type = ?, Rating = ?, Answer = ? \
        WHERE QuestionID = ?',Question)
    connection.commit()

    #The fnDeleteIncorrectAnswers function
    #deletes the incorrect answers for that question
def fnDeleteIncorrectAnswers(QuestionID):
    cursor.execute(
        'DELETE FROM tblIncorrectAnswers \
        WHERE IncAnsID IN (SELECT IncAnsID FROM tblQuestionIncorrectAnswers WHERE QuestionID = ?)',[QuestionID])
    connection.commit()

    #The fnDeleteQuestion function deletes
    #the question provided
def fnDeleteQuestion(QuestionID):
    cursor.execute(
        'DELETE FROM tblQuestions \
        WHERE QuestionID = ?', [QuestionID])
    connection.commit()

    #The fnFetchCategory function
    #fetches the category details 
def fnFetchCategory(CatID):
    cursor.execute(
        'SELECT Category,Recent_Score,CatID FROM tblCategory \
        WHERE CatID = ?',[CatID])
    return cursor.fetchall()

    #The fnUpdateScore function
    #updates the score for that
    #category
def fnUpdateScore(CatID,Score):
    cursor.execute(
        'UPDATE tblCategory \
        SET Recent_Score = ? \
        WHERE CatID = ?',[Score,CatID])
    connection.commit()

    #The fnFetchUserDetails function
    #fetches all user details for that user
def fnFetchUserDetails(Username):
    cursor.execute(
        'SELECT * FROM tblUsers \
        WHERE Username = ?',[Username])
    return cursor.fetchall()

    #The fnUpdatePassword function
    #updates the password for that user
def fnUpdatePassword(NewPassword,Username):
    cursor.execute(
        'UPDATE tblUsers\
        SET Password = ?\
        WHERE Username = ?',[NewPassword,Username])
    connection.commit()
    

#The following if statement is executed
#when the program is run directly by an interpreter
#and not as a module
if __name__ == '__main__':
    #A connection to the database
    #is made and the database is created
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    fnCreateDatabase(cursor)
    #A tkinter window is created
    #and passed on to the MainMenu class
    winMain = Tk()
    Mainmenu = MainMenu(winMain)
    winMain.mainloop()
    #The connection to the database is
    #closed when the window closed
    connection.close()
    
