from pydantic import BaseModel, Field


# Pydantic BaseModel for Data Validation while Submit / Update form request
class TodoRequest (BaseModel):
    title:          str     =   Field ( min_length = 3, max_length = 100 ) 
    description:    str     =   Field ( min_length = 3, max_length = 300 )
    priority:       int     =   Field ( gt = 0, lt = 6 )
    complete:       bool