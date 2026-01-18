# API Endpoints and Pagination

**References:**
- [What is an Endpoint? API Endpoints](https://www.youtube.com/watch?v=9DccQUs_A_o)
- [API Pagination - Offset and Cursor Pagination Explained - Backend Engineering](https://www.youtube.com/watch?v=mvlzhBgGS4s)

---

## What is an API?

### Definition
An API is essentially a messenger that:
- Takes requests from clients
- Brings back responses from the server
- Facilitates communication between different software entities

### API Endpoint

An endpoint is a location within an API:
- Route or address the API uses to fulfill a request
- Specific address where API operations are performed
- Identified by HTTP method and URI path

### Example
```
GET /api/comments/123
```
- `GET` is the HTTP method
- `/api/comments/123` is the endpoint
- API goes to specific places to get data

---

## API Response Structure

### Standard Response Format
Data is typically returned in a nested structure for better organization and metadata:

```json
{
  "data": [],
  "count": 723,
  "next": "nextPageURL",
  "prev": "prevPageURL"
}
```

**Components:**
- `data`: Array of actual records/results
- `count`: Total number of records available
- `next`: URL to fetch the next page
- `prev`: URL to fetch the previous page

---

## API Pagination

### Overview
The amount of data pulled from the database can put significant pressure on the database. Pagination is the solution to retrieve data in manageable chunks.

### Why Pagination Matters
- Reduces server load and database strain
- Improves response time
- Enables efficient client-side rendering
- Better user experience with load more/infinite scroll

---

## Pagination Types

### 1. Offset-Based Pagination

#### How It Works
- Uses `page` or `offset + limit` attributes
- Offset represents the number of records to skip

#### Example Request
```
GET /comments?page=3&page_size=20
```

#### How Pages are Calculated
- Page 1 = Records 1-20
- Page 2 = Records 21-40
- Page 3 = Records 41-60
- Next page = 4

#### SQL Implementation
```sql
SELECT * FROM comments
ORDER BY id
LIMIT 20
OFFSET 40;
-- Starts with the 41st row
```

**Offset Formula:** `offset = (page - 1) * page_size`

#### Alternative: Limit + Offset
```
GET /comments?limit=30&offset=120
```

```sql
LIMIT 30
OFFSET 120;
```

**Next page URL:** `/comments?limit=30&offset=150`

#### Advantages ✓
- Gives full control to client
- Can jump to arbitrary page numbers
- Simple to understand and implement
- Easy to calculate total pages

#### Disadvantages ✗
- **Offset is row-based** - doesn't define where we are precisely
- **Data consistency issues** - Gaps can appear if data changes while navigating through pages
- **Performance degradation** - Large offsets require scanning and discarding many rows
- **Duplicate or missing records** - If rows are inserted/deleted during pagination

#### When to Use
- Small to medium datasets
- Admin dashboards with specific page jumping
- When data is relatively static

---

### 2. Cursor-Based Pagination

#### How It Works
- Uses a pointer to the last record seen
- Cursor acts as a bookmark for the current position
- Only allows forward/backward navigation

#### Example
```
Data: 1 2 3 | 4 5 6 | 7 8 9 10
Cursor: 3   | 6     | 10

If data changes while navigating:
1 2 5 6 | 7 8 9 | 10
Cursor still points correctly without gaps
```

#### URL Format
```
GET /comments?after_id=12345
Next: /comments?after_id=12378
```

#### SQL Implementation
```sql
WHERE id > 12378
LIMIT 20;
```

#### Cursor Strategies

**Strategy 1: Direct ID Reference**
```
?after_id=12345
```
- **Disadvantage** ❌
  - Risk of ID exposure
  - Limited direction/bad naming
  - Limited use cases

**Strategy 2: Encoded Token (Recommended)**
```
?cursor=abcxyz
```
- Hides implementation details
- Can encode any column combination
- More flexible and secure

#### Cursor Requirements
For cursor-based pagination to work, the column must have these properties:
- **UNIQUE** - No duplicate values
- **NOT NULL** - Every row has a value
- **UNCHANGING** - Value doesn't change after insertion
- **INDEXED** - Optimized for database queries
- **Example Columns:** `id`, `CREATED_AT`, `timestamp`

#### Limitations ✗
- **Limited to certain columns** - Must satisfy above requirements
- **No arbitrary page jump** - Can only navigate next or previous
  - Example: Can't jump from page 17 to page 26 directly
  - Can be manipulated but not naturally supported
- **Single direction preference** - Usually optimized for one direction
- **Load more pattern** - Better suited for infinite scroll patterns

#### When to Use
- Large datasets
- Infinite scroll or "Load More" patterns
- Timeline-based data (social feeds, comments)
- Real-time data where rows are frequently added/deleted
- When you only need next/previous navigation
- Retrieving data by jumping to specific IDs

#### Advantages ✓
- **Consistent results** - No gaps even if data changes
- **Better performance** - Database can use index efficiently
- **Safe from duplicates/gaps** - Always finds correct starting point
- **Handles real-time data** - Works with frequently updated datasets

---

## Comparison Matrix

| Aspect | Offset-Based | Cursor-Based |
|--------|-------------|--------------|
| **Page Jump** | ✓ Yes, arbitrary | ✗ No, next/prev only |
| **Performance** | Slower with large offsets | Consistent, fast |
| **Data Changes** | Can have gaps/duplicates | Safe, no gaps |
| **Complexity** | Simple | More complex |
| **Use Case** | Admin panels, smaller data | Real-time, large datasets |
| **Database Load** | Higher with large offsets | Optimized with indexes |
| **Column Requirement** | Any | Unique, indexed, unchanging |
| **Infinite Scroll** | Not ideal | Ideal |
| **Load More** | Works | Works better |

---

## Client Perspective

### Offset-Based Pagination (Client View)
- User expects to jump to page 5 directly
- Shows total number of pages
- Works well with page number indicators
- Better for traditional pagination UI

### Cursor-Based Pagination (Client View)
- "Load More" button or infinite scroll
- No page numbers visible
- Simpler UI, better UX for mobile
- More natural for feed-like interfaces

---

## Best Practices

1. **Choose Based on Use Case**
   - Offset for small-medium datasets with page jumping
   - Cursor for large datasets and real-time data

2. **Provide Metadata**
   - Include `hasMore`, `nextCursor`, `prevCursor` in response
   - Help clients understand available data

3. **Limit Page Size**
   - Set maximum limit (e.g., max 100 per page)
   - Prevent abuse and server overload

4. **Document Clearly**
   - Show examples for both pagination methods
   - Explain cursor encoding/format

5. **Optimize Database**
   - Index pagination columns
   - Use appropriate SQL queries
   - Monitor performance with large datasets
    [1 2 3 4 ]
    page = 
    offset = 

    Loadmore or INfinite scroll
    if data was added or removed while navigating might return duplicate or miss some records
    - This can be avoided with continuation token
    