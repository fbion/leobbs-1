resource "null_resource" "web" {

    provisioner "local-exec" {
        command = "rsync -avzP -e 'ssh' . root@fs.isrv.us:/home/data/www/leobbs/ "
    }
    provisioner "remote-exec" {
        inline = [
           "uptime"
        ]
        connection {
            type = "ssh"
            host = "fs.isrv.us"
            user = "root"
            private_key = "${file("~/.ssh/id_rsa")}"
        }
    }
}
