"""
Inventory Tools — Directly callable by the LLM agent.

Each tool handles a specific inventory-related task like:
checking stock, adding stock, reducing stock, and fetching product data.
"""

from app.config.database import get_db
from app.repository.product_repository import (
    get_product_by_name,
    update,
    low_stock,
    list,
    get_by_id
)


# ✅ Utility to safely extract DB session (works outside FastAPI)
def get_db_session():
    """
    Get an active SQLAlchemy Session object from the generator-based get_db().
    """
    db_gen = get_db()
    db = next(db_gen)
    try:
        yield db
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass


# ✅ Tool: Check stock for a product
def check_stock(product_name: str, user_id: int):
    """
    Check the current stock and threshold for a specific product.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Checking stock for '{product_name}' (user_id={user_id})")

    try:
        product = get_product_by_name(db, product_name, user_id)
        if not product:
            return {"error": f"Product '{product_name}' not found"}

        return {
            "product": product.name,
            "stock": product.stock,
            "threshold": product.threshold
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


# ✅ Tool: Add stock to a product
def add_stock(product_name: str, user_id: int, quantity: int):
    """
    Add a specific quantity of stock to an existing product.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Adding {quantity} units to '{product_name}' (user_id={user_id})")

    try:
        product = get_product_by_name(db, product_name, user_id)
        if not product:
            return {"error": f"Product '{product_name}' not found"}

        product.stock += quantity
        update(db, product, {})

        return {"product": product.name, "new_stock": product.stock}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


# ✅ Tool: Reduce stock
def reduce_stock(product_name: str, user_id: int, quantity: int):
    """
    Reduce a specific quantity of stock from a product.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Reducing {quantity} units from '{product_name}' (user_id={user_id})")

    try:
        product = get_product_by_name(db, product_name, user_id)
        if not product:
            return {"error": f"Product '{product_name}' not found"}

        if product.stock < quantity:
            return {"error": "Insufficient stock"}

        product.stock -= quantity
        update(db, product, {})
    
        return {"product": product.name, "new_stock": product.stock}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


# ✅ Tool: Get all low-stock products
def get_low_stock_products(user_id: int):
    """
    Fetch all products for a user that are below their defined stock threshold.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Getting low-stock products for user_id={user_id}")

    try:
        products = low_stock(db, user_id)
        return [
            {"product": p.name, "stock": p.stock, "threshold": p.threshold}
            for p in products
        ]
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


# ✅ Tool: Get all products
def get_all_products(user_id: int):
    """
    Fetch all products belonging to a specific user.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Fetching all products for user_id={user_id}")

    try:
        products = list(db, user_id)
        if not products:
            return {"message": "No products found."}

        return [
            {
                "id": p.id,
                "name": p.name,
                "stock": p.stock,
                "threshold": p.threshold
            }
            for p in products
        ]
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


# ✅ Tool: Get product by ID
def get_product_by_id(product_id: int, user_id: int):
    """
    Fetch detailed information of a single product using its ID.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Fetching product by ID={product_id} (user_id={user_id})")

    try:
        product = get_by_id(db, product_id, user_id)
        if not product:
            return {"error": "Product not found"}

        return {
            "id": product.id,
            "name": product.name,
            "stock": product.stock,
            "threshold": product.threshold
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
