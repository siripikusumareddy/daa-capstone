# test_install.py
print("Testing installations...")

try:
    import flask
    print(f"✅ Flask version: {flask.__version__}")
except:
    print("❌ Flask not installed")

try:
    import numpy
    print(f"✅ NumPy version: {numpy.__version__}")
except:
    print("❌ NumPy not installed")

try:
    import matplotlib
    print(f"✅ Matplotlib version: {matplotlib.__version__}")
except:
    print("❌ Matplotlib not installed")

print("\nTesting imports...")
try:
    from backend.segnment_tree import SegmentTree
    print("✅ SegmentTree imported")
    
    from backend.signal_processor import SignalProcessor
    print("✅ SignalProcessor imported")
    
    from backend.app import app
    print("✅ App imported")
    
    print("\n🎉 All good! Ready to run!")
except Exception as e:
    print(f"❌ Import error: {e}")
