# Game On Local Network

Local ağda oynayabileceğim oyunlar yapmak için öncelikle tasarlayacağım yapıyı oldukça basitleştirmeye karar verdim ve kodun arka planında yapılacak temel işlevin **server** ve **client**lar arasındaki mesajlaşmanın sağlanması olduğunu gördüm. Bu yüzden geliştirmeye clientlar arasındaki *sıralı mesajlaşmayı* sağlayacak bir yapı üzerinden başladım.

## Sıralı Mesajlaşma

**Server** kodu çalışmaya başladığında, *broadcast* ile 3 saniyede 1 kez paket gönderecek ve clientlardan gelen bağlantı isteklerini dinleyecek fonksiyonları ayrı threadler olarak başlatacak şekilde başlar. Server başladıktan sonra başlatılan clientlar, 5000 portundan gelecek paketleri dinlemeye başlar ve eğer gelen paket **"Eren12345"** ise, gelen paketin adresine 5555 portundan bağlantı isteği atar. Server, halihazırda bağlantı isteklerini dinlediği için TCP socket bağlantısı kurulmuş olur. Server, 2. bağlantı kurulana kadar herhangi bir işleme başlamaz. 

![Pasted image (3)](https://github.com/user-attachments/assets/2c65deb3-cbe4-4105-9d84-951e07ffca1c)

## Flag Yapısı

Sıranın kimde olduğunu clientlara bildirmek için gönderdiğim paketlerin ilk byte'ını **flag** olarak kullanmayı düşündüm. 2. bağlantı kurulduktan sonra server; önce bağlanan client'a ilk byte'ı 1 olan, diğer client'a ise 0 olan bir paket gönderiyor. Bu ilk gelen paket'e göre clientlar kendi ID'lerini flag 1 ise id=0, flag 0 ise id=1 (ilk bağlanan 0, diğerinin 1) olacak şekilde belirliyorlar. Ardından gönderilen mesajların ilk byte'larına bakılarak sıranın kimde olduğu kontrol edilmeye devam ediyor ve sırası gelen mesaj gönderiyor. Client'ın gönderdiği mesaj önce server'a gidiyor, sonra server 2 client'a birden flagleri ile birlikte mesaj gönderiyor.

![Pasted image (2)](https://github.com/user-attachments/assets/4a07bb9c-b14e-4e27-947b-1a967292eb3a)

## XOX Oyunu

Mesajlaşma kısmını tamamladıktan bu yapıyı xox oyununa uygulamaya geçtim.GPT'ye yaptırdığım bir ui ile kullanıcıların yaptığı hamleleri mesaj gönderimi için kullanılan yerlerden göndererek oyunu tamamladım

![image](https://github.com/user-attachments/assets/00bfc0af-5eb5-4a3c-a291-5baa9adaf886)


