#-------------------------------------------------------------------------------------
#   Non permanent models (RESOURCE)
#   Regarding non-perma models and is a type of resource (actors/entities)
#   This directory is for RESOURCES ONLY, that is, models that are non-permanent.
#   Please do not add anything other than forms/database-models here.
#   introduced in u3
#-------------------------------------------------------------------------------------

#   Current Models in system:
*Please add to this list.
-resource
  -geores
    $geopoint
    $geopath
    $georoute
  $COPY_template

The COPY_template.py is available to start creating resources

1. copy the template into a desired subfolder and rename it to something easy
2. Follow the instructions in COPY_template and define the model, addform and editform
3. After that, proceed to rdef.py and add in the new resource.
4. Add in the links on __sidebar so that you may access it
5. verify your model!
