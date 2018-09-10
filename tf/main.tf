resource "null_resource" "web" {

    provisioner "file" {
        source = "/mnt/d/workspace/netroby/leobbs"
        destination = "/home/data/www"
    connection {
        type = "ssh"
        host = "fs.isrv.us"
        user = "root"
        private_key = "${file("~/.ssh/id_rsa")}"
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
