from typing import Optional
from app import models, oauth2, schemas
from app.database import get_db # import the get_db function from database
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, APIRouter
from typing import List
from sqlalchemy import func

# create the router for employee (app.include_router(employee.router) in main.py) @app will be replaced by router
router = APIRouter(
    prefix = "/posts", # prefix for the router helps to reduce the code
    tags = ["Posts"] # tags for the router helps to group the router
) 

@router.get("/", response_model=List[schemas.PostOut]) # get all the posts (app.get("/posts") in main.py)
def read_posts(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)


    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)

    return posts

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post) # create a new employee (app.post("/posts") in main.py)
def create_post(post: schemas.AddPost, db: Session= Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)): # current_user is the user who is logged in
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute("""INSERT INTO posts (name, place, employed) VALUES (%s, %s, %s) RETURNING * """, (employee.name, employee.place, employee.employed))
    # employee_dict = employee.dict()
    # employee_dict['id'] = randrange(0, 1000000)
    # my_emps.append(employee_dict)
    # new_employee = cursor.fetchone()
    # conn.commit()
    return new_post



@router.get("/{id}", response_model= schemas.PostOut, status_code= status.HTTP_202_ACCEPTED) # get an employee by id (app.get("/posts/{id}") in main.py)
def get_post(id: int, db: Session= Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM posts WHERE id= %s """, (id,))
    # employee = cursor.fetchone()
    # employee = find_employee(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"employee with id: {id} was not found"}

    # if employee.owner_id != current_user.id:
    #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    print(post)
    return post


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT) # delete an employee by id (app.delete("/posts/{id}") in main.py)
def delete_post(id: int, db: Session= Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)): # current_user is the user who is logged in

    post = db.query(models.Post).filter(models.Post.id == id)

    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING * """, (id,))
    # emp = cursor.fetchone()
    # conn.commit()

    # index = find_index_employee(id)
    if post.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exists")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    
    # my_emps.pop(index)
    post.delete(synchronize_session=False)
   
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code= status.HTTP_202_ACCEPTED, response_model=schemas.Post) # update an employee by id (app.put("/posts/{id}") in main.py)
def update_post(id: int, addpost: schemas.AddPost, db: Session= Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):

    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post = updated_post.first()
    # cursor.execute("""UPDATE posts SET name= %s, place= %s, employed=%s WHERE id= %s RETURNING * """, (employee.name, employee.place, employee.employed, id,))
    # updated_employee = cursor.fetchone()
    # conn.commit()
    # index = find_index_employee(id)
    if post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exits")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # employee_dict = employee.dict()
    # employee_dict['id'] = id
    # my_emps[index] = employee_dict
    updated_post.update(addpost.model_dump(), synchronize_session= False)
    db.commit()
    return updated_post.first()