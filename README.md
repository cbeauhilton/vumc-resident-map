
How to get the pics in the map (adapted from Simon's website):

```sql

select json_object(
  'image', img || '?w=800&h=400&fit=crop',
  'title', name,
  'description', substr(bio, 0, 200),
  ) as popup,
  latitude, longitude from folks

```
