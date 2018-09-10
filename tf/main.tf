resource "null_resource" "web" {

    provisioner "file" {
        source = "/mnt/d/workspace/netroby/leobbs"
        destination = "/home/data/www/"
    connection {
        type = "ssh"
        host = "fs.isrv.us"
        user = "root"
        private_key = "${file("~/.ssh/id_rsa")}"
        bastion_host = "la.isrv.us"
        bastion_port = "23333"
        bastion_user = "huzhifeng"
        bastion_private_key = "${file("~/.ssh/id_rsa")}"
    }

    } 
    connection {
        type = "ssh"
        host = "fs.isrv.us"
        user = "root"
        private_key = "${file("~/.ssh/id_rsa")}"
    }
    provisioner "remote-exec" {
        inline = [
           "uptime"
        ]
    }
}
