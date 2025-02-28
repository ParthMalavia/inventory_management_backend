# inventory_management_backend

### Run the FastAPI App

1. **Install Requirements**  
   - Run `pip install -r requirements.txt` to install all required packages.

2. **Run the App**  
   - Run `uvicorn app.main:app --reload` to start the FastAPI application. 
   NOTE: The `--reload` flag will automatically reload the app if you make any changes to the source code.

When you make changes to your existing models (e.g., `User`, `Inventory`, `Category`) or add a new model in your FastAPI application with Alembic, you need to follow a consistent process to update your database schema. Here's the step-by-step workflow you should run every time:

---

### Workflow for Model Changes or New Models

1. **Update or Add the Model**  
   - Modify the existing model (e.g., add a new column to `app/models/inventory.py`) or create a new model file (e.g., `app/models/supplier.py`).
   - Ensure the model is imported in `alembic/env.py` so Alembic can detect it. For example, if you add a `Supplier` model, update `env.py`:
     ```python
     from app.models import user, inventory, category, supplier  # Add new model here
     ```

2. **Generate a New Migration Script**  
   - Run the following command in the `backend/` directory to autogenerate a migration script based on your model changes:
     ```bash
     alembic revision --autogenerate -m "Description of your change"
     ```
     - Replace `"Description of your change"` with a meaningful message, e.g., `"Add supplier table"` or `"Add column to inventory"`.
   - This creates a new file in `alembic/versions/` (e.g., `xxxx_add_supplier_table.py`).

3. **Review the Migration Script**  
   - Open the generated script in `alembic/versions/` and verify it correctly reflects your changes.
   - Alembic’s autogeneration is good but not perfect—it might miss some changes (e.g., complex constraints or index renames). Edit the `upgrade()` and `downgrade()` functions if necessary.

4. **Apply the Migration**  
   - Run this command to apply the migration to your database:
     ```bash
     alembic upgrade head
     ```
   - This updates your database schema to match your models.

5. **Test Your Application**  
   - Start your FastAPI app (`python main.py`) and test the affected endpoints to ensure the changes work as expected.

---

### Example Scenarios

#### Scenario 1: Adding a New Column to an Existing Model
Suppose you add a `location` column to the `Inventory` model in `app/models/inventory.py`:
```python
class Inventory(Base):
    __tablename__ = "inventory"
    # Existing fields...
    location = Column(String, nullable=True)  # New column
```

Steps:
1. Update `app/models/inventory.py` with the new column.
2. Generate migration:
   ```bash
   alembic revision --autogenerate -m "Add location column to inventory"
   ```
   Generated script (`alembic/versions/xxxx_add_location_column_to_inventory.py`):
   ```python
   def upgrade():
       op.add_column('inventory', sa.Column('location', sa.String(), nullable=True))

   def downgrade():
       op.drop_column('inventory', 'location')
   ```
3. Apply migration:
   ```bash
   alembic upgrade head
   ```

#### Scenario 2: Adding a New Model
Suppose you add a `Supplier` model in `app/models/supplier.py`:
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

Steps:
1. Create `app/models/supplier.py`.
2. Update `alembic/env.py` to import the new model:
   ```python
   from app.models import user, inventory, category, supplier
   ```
3. Generate migration:
   ```bash
   alembic revision --autogenerate -m "Add supplier table"
   ```
   Generated script (`alembic/versions/xxxx_add_supplier_table.py`):
   ```python
   def upgrade():
       op.create_table(
           'suppliers',
           sa.Column('id', sa.Integer(), nullable=False),
           sa.Column('name', sa.String(), nullable=False),
           sa.Column('contact_info', sa.String(), nullable=True),
           sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
           sa.PrimaryKeyConstraint('id')
       )
       op.create_index(op.f('ix_suppliers_id'), 'suppliers', ['id'], unique=False)

   def downgrade():
       op.drop_table('suppliers')
   ```
4. Apply migration:
   ```bash
   alembic upgrade head
   ```

---

### Commands to Run Every Time
Here’s the condensed list of commands you’ll run after making changes to models or adding new ones:

1. **Generate Migration**:
   ```bash
   alembic revision --autogenerate -m "Your change description"
   ```

2. **Apply Migration**:
   ```bash
   alembic upgrade head
   ```

---

### Additional Tips
- **Review Before Applying**: Always check the generated migration script to ensure it matches your intent. Autogeneration might not catch everything (e.g., renaming a column requires manual edits).
- **Revert if Needed**: If something goes wrong, revert the last migration:
  ```bash
  alembic downgrade -1
  ```
- **Multiple Changes**: If you make several changes at once (e.g., modify `Inventory` and add `Supplier`), you can group them into one migration by running `alembic revision --autogenerate` after all changes are made.
- **Database Reset**: To start fresh (e.g., for testing), drop the database and reapply all migrations:
  ```bash
  alembic downgrade base  # Reset to no tables
  alembic upgrade head    # Apply all migrations
  ```
