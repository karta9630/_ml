# Hebbian分類製作
Hebbian主要計算分類後的權重，以方便後續數據的分類。
使用ChatGpt完成，並理解，此程式碼使用Hebbian建立兩類的資料，並分為+1以及-1兩個標籤，將這些資料合併後進行權重的計算
w = lr * data的向量 * 標籤   --data為 [2,3]、[-2,5]、[1,0]之類的
此時若有一筆新的資料要預測在哪個類別，只需要
w * newdata  若>0則為 +1標籤 
