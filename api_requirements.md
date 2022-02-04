# API Requirements

## CRUD endpoints

### Create
	* New User
		POST /users
	* New Blog post
		POST /Blogs
	* New Comment
		POST /Blogs/:id/Comments/
	* New Like
		POST /Blog
### Read
	* User info
		GET /Users/:id
	* Blog post
		GET /Blogs/:id
	* Comment text
		GET /Comments/:id
	* Comments related to a single blog post
		GET /Blogs/:id/Comments
	* Comments related to a single user
		GET /Users/:id/Comments
	* Likes on a specific blog
		GET /Blogs/:id/Likes
	* Likes on a specific comment
		GET /Comments/:id/Likes
	* See a users blogs
		GET /Users/:id/Blogs
	* See a users liked blogs
		GET /Users/:id/Blogs/Likes
	* See a users liked comments
		GET /Users/:id/Comments/Likes

### Update
	* Update blog (add edited tag)
		PATCH/PUT /Blogs/:id
	* Update comment (add edited tag)
		PATCH/PUT /Comments/:id
	* Change user info / Change password
		PATCH/PUT /Users/:id

### Delete
	* User
	* Blog post
	* Comment
	* Like