This readme file stores version information as well as
features and changelogs. pls keep this up to date whenever
you commit.

use pip3 (python3-pip) to install the following modules
flask
flask_wtf
flask_sqlalchemy
flask_bootstrap
flask_login
flask_admin
flask_io
flask_socketio

changelogs formatting
update<N>	<date:DD/MM/YY>---<time>
+	new updates
-	bug fixes
$	suggested
TODO:	todo
*	notice

*Please format your updates accordingly so that we can view the changes
*easily. also comment on the code and functionality of some lines
*for labels of R1 - R9, they're are of the previous version of pyFlask
*please ignore. we will use U0 - Un to denote versions for this system

------------------------------------------------------------------------------------
---------------------------------CHANGELOGS-----------------------------------------

update0		08/12/18---1:22pm
[+	ported old pyflask server to setup petabus
[	  ported useradd/userlist/usermod
[ 	ported home
[   ported admintools
[   ported models/sqlite engine
[+	initialized git repo
[+	added new pkg architectures
[	  source.py to provide the flask object
[   introduced blueprinting, refer to flask
[   introduced seperate wrapper files
[	  flim.py renamed to limits.py
[   const.py added to store constant vals
[	  old changelogs can be viewed at pyFlask_old.txt (from pyflask)
[$	new db models
[$  revamp templates structure

update1   12/12/18---11:04pm
[+  ported flog.py from old pyflask to servlog.py
[+  added finally: clause in server.py (main)

update2   09/01/19---10:26pm
[+  Major pkg system revamp
[   subdir added to further subdivide and clear up the pkg dir
[   template file system also followed suite, now classed by directory
[   improved the javascript src and css files, using include directory to import
[+  ported flask socketio
[   new system time clock (for testing)
[+  introduced a mapping module (leaflet)
[-  fixed some old .static problem : .static -> static, reference error
[   this bug fix comes along with the template dir revamp
[$  introduce universal sysres mechanics
TODO: Mapping system to now get location from db
TODO: flask-socket io to update map location without refresh

update3   10/01/19---06:49pm
[+  generalized sysres mechanics
[   refer to readme in /resource directory under pkg
[   now only add py files and define your models.
[   remember to add link in includes/_sidebar.html
[+  admintools/resetdb route now resets the database without deleting manually

update4   23/01/19---22:53pm
[+  changed the admin pri mechanism, now an integer which specifies the privilege level
[   Users are actually mapped to a userType class, with userType id 1 defaulting to admin
[   This allows generic defining of custom user classes
[+  token generation mechanism now added to allow user to register without admin access
[   The administrator generates the URL to allow users to register/change password
[-  Fixed the datatables error, now we can sort and list the datatables

update5   31/01/19---01:00am
[+  restructured the template directory
[   now the template consist of bootstrap gentelella and bootstrap leaflet
[   both serve different purposes, leaflet being the mapping while gentelella std
[   dashboard. fixed some UI and html errors, as well as better formatting for some.
