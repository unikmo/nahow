<?php
// NAHOW contact form: sends one email to mail@nahow.de. Nothing is stored on the server.
const TO = 'mail@nahow.de';
function back($ok) { header('Location: /kontakt/' . ($ok ? 'danke/' : 'fehler/'), true, 303); exit; }
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { header('Location: /kontakt/', true, 303); exit; }
// Spam traps: hidden field must be empty; form must have been open for at least 3 seconds.
if (!empty($_POST['website'])) back(true);
$ts = (int)($_POST['ts'] ?? 0);
if ($ts < 1 || time() - $ts < 3 || time() - $ts > 86400) back(false);
$name = trim(preg_replace('/[\r\n]+/', ' ', (string)($_POST['name'] ?? '')));
$mail = trim((string)($_POST['email'] ?? ''));
$msg  = trim((string)($_POST['message'] ?? ''));
if ($name === '' || $msg === '' || empty($_POST['consent'])) back(false);
if (!filter_var($mail, FILTER_VALIDATE_EMAIL) || preg_match('/[\r\n]/', $mail)) back(false);
if (mb_strlen($name) > 120 || mb_strlen($mail) > 200 || mb_strlen($msg) > 5000) back(false);
// Simple rate limit: one message per visitor per 60 seconds.
$key = sys_get_temp_dir() . '/nahow_cf_' . md5($_SERVER['REMOTE_ADDR'] ?? '');
if (is_file($key) && time() - filemtime($key) < 60) back(false);
$subject = '=?UTF-8?B?' . base64_encode('Anfrage über nahow.de') . '?=';
$body = "Name: $name\nE-Mail: $mail\n\n$msg\n";
$replyName = '=?UTF-8?B?' . base64_encode($name) . '?=';
$headers = "From: NAHOW Kontaktformular <noreply@nahow.de>\r\nReply-To: $replyName <$mail>\r\n" .
           "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n";
$ok = @mail(TO, $subject, $body, $headers);
if ($ok) @touch($key);
back($ok);
