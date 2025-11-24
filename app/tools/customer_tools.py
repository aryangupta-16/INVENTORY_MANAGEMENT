"""
Customer Tools — Directly callable by the LLM agent.

Each tool handles a specific customer-related task like:
creating/deleting customers, fetching customer data, and managing purchases.
"""

from app.config.database import get_db
from app.repository.customer_repository import (
    create_customer,
    delete_customer,
    get_customers,
    get_customer,
    get_customer_by_phone,
    add_purchase,
    get_customer_purchases
)
from app.schema.CustomerSchema import CustomerCreate


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


# ----------------- Customer Tools -----------------

def create_new_customer(user_id: int, customer_data: CustomerCreate):
    """
    Create a new customer for a given user.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Creating new customer (user_id={user_id})")

    try:
        customer = create_customer(db, user_id, customer_data)
        return {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def remove_customer(user_id: int, customer_id: int):
    """
    Delete a customer by ID for a specific user.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Deleting customer ID={customer_id} (user_id={user_id})")

    try:
        customer = get_customer(db, user_id, customer_id)
        if not customer:
            return {"error": "Customer not found"}
        delete_customer(db, customer)
        return {"message": f"Customer {customer.name} deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def fetch_all_customers(user_id: int):
    """
    Fetch all customers belonging to a user.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Fetching all customers for user_id={user_id}")

    try:
        customers = get_customers(db, user_id)
        return [
            {"id": c.id, "name": c.name, "phone": c.phone}
            for c in customers
        ] if customers else {"message": "No customers found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def fetch_customer_by_phone(user_id: int, phone: str):
    """
    Fetch a single customer by phone number.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Fetching customer by phone={phone} (user_id={user_id})")

    try:
        customer = get_customer_by_phone(db, user_id, phone)
        if not customer:
            return {"error": "Customer not found"}
        return {"id": customer.id, "name": customer.name, "phone": customer.phone}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def record_purchase(user_id: int, customer_id: int, product_id: int, quantity: int, paid: int):
    """
    Add a purchase for a customer and reduce product stock.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Recording purchase for customer_id={customer_id}, product_id={product_id} (user_id={user_id})")

    try:
        purchase = add_purchase(db, user_id, customer_id, product_id, quantity, paid)
        if not purchase:
            return {"error": "Purchase failed (check customer, product, stock)"}
        return {
            "purchaseId": purchase.id,
            "customerId": purchase.customer_id,
            "productId": purchase.product_id,
            "quantity": purchase.quantity,
            "totalPrice": purchase.price,
            "paid": purchase.paid,
            "date": purchase.created_at.isoformat() if hasattr(purchase, "created_at") else None
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


def fetch_customer_purchases(user_id: int):
    """
    Fetch all customer purchases for a user.
    """
    db = next(get_db_session())
    print(f"🧰 Tool: Fetching all purchases for user_id={user_id}")

    try:
        purchases = get_customer_purchases(db, user_id)
        return purchases if purchases else {"message": "No purchases found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
