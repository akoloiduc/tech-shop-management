use ShopManagement;
update PurchaseOrder
set Status = 'Ordered' where Status = 'Processing'
update PurchaseOrder
set Status = 'Ordered' where Status = 'Cancelled'
