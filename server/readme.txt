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
>	additional notice


*Please format your updates accordingly so that we can view the changes
*easily. also comment on the code and functionality of some lines
*for labels of R1 - R9, they're are of the previous version of pyFlask
*please ignore. we will use U0 - Un to denote versions for this system

------------------------------------------------------------------------------------
---------------------------------CHANGELOGS-----------------------------------------

update0		08/12/18---1:22pm
[+	ported old pyflask server to setup petabus
[	  >ported useradd/userlist/usermod
[ 	>ported home
[   >ported admintools
[   >ported models/sqlite engine
[+	initialized git repo
[+	added new pkg architectures
[	  >source.py to provide the flask object
[   >introduced blueprinting, refer to flask
[   >introduced seperate wrapper files
[	  >flim.py renamed to limits.py
[   >const.py added to store constant vals
[	  >old changelogs can be viewed at pyFlask_old.txt (from pyflask)
[$	new db models
[$  revamp templates structure

update1   12/12/18---11:04pm
[+  ported flog.py from old pyflask to servlog.py
[+  added finally: clause in server.py (main)

update2   09/01/19---10:26pm
[+  Major pkg system revamp
[   >subdir added to further subdivide and clear up the pkg dir
[   >template file system also followed suite, now classed by directory
[   >improved the javascript src and css files, using include directory to import
[+  ported flask socketio
[   >new system time clock (for testing)
[+  introduced a mapping module (leaflet)
[-  fixed some old .static problem : .static -> static, reference error
[   >this bug fix comes along with the template dir revamp
[$  introduce universal sysres mechanics
TODO: Mapping system to now get location from db
TODO: flask-socket io to update map location without refresh

update3   10/01/19---06:49pm
[+  generalized sysres mechanics
[>  refer to readme in /resource directory under pkg
[>  now only add py files and define your models.
[>  remember to add link in includes/_sidebar.html
[+  admintools/resetdb route now resets the database without deleting manually
