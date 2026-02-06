# Pagination Analysis – GitHub API

## Endpoint used
https://api.github.com/users/octocat/repos

per_page=3

---

## Page 1
URL:
?page=1&per_page=3

Result:
- 3 repos returned

Link header:
- next
- last

Meaning:
More pages available

---

## Page 2
URL:
?page=2&per_page=3

Result:
- 3 repos returned

Link header:
- next
- prev
- first
- last

Meaning:
Middle page

---

## Page 3
URL:
?page=3&per_page=3

Result:
- remaining repos returned

Link header:
- prev
- first

Meaning:
Last page

---

## Learnings
- Pagination splits large data
- Improves performance
- Avoids heavy response
- Used in GitHub, Instagram, etc.
