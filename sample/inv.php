<?php
// ==========================================
// Build: 2026-10-01 17:00:00
// Changes: 1 of 4
// Location: /test_nrz/inv.php
// ==========================================

// محاسبات
$total = 0;
$rows = array();
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $customer = trim(isset($_POST['customer']) ? $_POST['customer'] : '');
    $product  = trim(isset($_POST['product'])  ? $_POST['product']  : '');
    $qty      = (int)(isset($_POST['qty'])     ? $_POST['qty']      : 0);
    $price    = (float)(isset($_POST['price']) ? $_POST['price']    : 0);

    if ($customer === '' || $product === '' || $qty <= 0 || $price <= 0) {
        $error = 'لطفاً همه فیلدها را به‌درستی پر کنید.';
    } else {
        $rowTotal = $qty * $price;
        $rows[] = array(
            'customer' => $customer,
            'product'  => $product,
            'qty'      => $qty,
            'price'    => $price,
            'rowTotal' => $rowTotal,
        );
        $total = $rowTotal;
    }
}
?>
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فاکتور فروش</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <link rel="stylesheet" href="assets/css/weather.css">
</head>
<body>
<div class="app-wrapper">

    <!-- ========== ویجت اب و هوا (ماژولار) ========== -->
    <section class="weather-widget" id="weather-widget" data-lat="35.6892" data-lon="51.3890" data-city="تهران">
        <div class="weather-widget__loader" id="weather-loader">در حال دریافت اب و هوا...</div>
        <div class="weather-widget__content" id="weather-content" hidden>
            <div class="weather-widget__main">
                <span class="weather-widget__icon" id="weather-icon">☀️</span>
                <div class="weather-widget__info">
                    <span class="weather-widget__temp" id="weather-temp">--</span>
                    <span class="weather-widget__city" id="weather-city">--</span>
                </div>
            </div>
            <div class="weather-widget__details">
                <span class="weather-widget__detail">رطوبت: <b id="weather-humidity">--</b>%</span>
                <span class="weather-widget__detail">باد: <b id="weather-wind">--</b> km/h</span>
            </div>
        </div>
    </section>

    <!-- ========== فرم صدور فاکتور ========== -->
    <section class="card">
        <header class="card__header">
            <h1 class="card__title">صدور فاکتور</h1>
        </header>

        <div class="card__body">

            <?php if ($error): ?>
                <div class="alert alert--error"><?php echo htmlspecialchars($error); ?></div>
            <?php endif; ?>

            <form method="post" class="form">
                <div class="form__group">
                    <label class="form__label" for="customer">نام مشتری</label>
                    <input class="form__input" type="text" id="customer" name="customer"
                           value="<?php echo htmlspecialchars(isset($_POST['customer']) ? $_POST['customer'] : ''); ?>" required>
                </div>

                <div class="form__group">
                    <label class="form__label" for="product">نام کالا</label>
                    <input class="form__input" type="text" id="product" name="product"
                           value="<?php echo htmlspecialchars(isset($_POST['product']) ? $_POST['product'] : ''); ?>" required>
                </div>

                <div class="form__row">
                    <div class="form__group">
                        <label class="form__label" for="qty">تعداد</label>
                        <input class="form__input" type="number" id="qty" name="qty" min="1"
                               value="<?php echo htmlspecialchars(isset($_POST['qty']) ? $_POST['qty'] : ''); ?>" required>
                    </div>

                    <div class="form__group">
                        <label class="form__label" for="price">قیمت واحد (تومان)</label>
                        <input class="form__input" type="number" id="price" name="price" min="1" step="1000"
                               value="<?php echo htmlspecialchars(isset($_POST['price']) ? $_POST['price'] : ''); ?>" required>
                    </div>
                </div>

                <button class="btn btn--primary" type="submit">ثبت فاکتور</button>
            </form>

        </div>
    </section>

    <!-- ========== پیش‌فاکتور ========== -->
    <?php if (!empty($rows)): ?>
    <section class="card">
        <header class="card__header">
            <h1 class="card__title">پیش‌فاکتور</h1>
        </header>

        <div class="card__body">
            <div class="table-wrapper">
                <table class="table">
                    <thead class="table__head">
                        <tr>
                            <th>مشتری</th>
                            <th>کالا</th>
                            <th>تعداد</th>
                            <th>قیمت واحد</th>
                            <th>جمع</th>
                        </tr>
                    </thead>
                    <tbody class="table__body">
                        <?php foreach ($rows as $r): ?>
                        <tr>
                            <td><?php echo htmlspecialchars($r['customer']); ?></td>
                            <td><?php echo htmlspecialchars($r['product']);  ?></td>
                            <td><?php echo number_format($r['qty']);         ?></td>
                            <td><?php echo number_format($r['price']);       ?></td>
                            <td class="table__cell--strong"><?php echo number_format($r['rowTotal']); ?></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>

            <div class="total-box">
                <span class="total-box__label">مبلغ قابل پرداخت:</span>
                <span class="total-box__value"><?php echo number_format($total); ?> تومان</span>
            </div>

            <button class="btn btn--secondary" onclick="window.print()">چاپ فاکتور</button>
        </div>
    </section>
    <?php endif; ?>

</div>

<script src="assets/js/weather-config.js"></script>
<script src="assets/js/weather.js"></script>
</body>
</html>