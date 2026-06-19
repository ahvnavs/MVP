terraform {
    backend "s3" {
        bucket = ""
        encrypt = true
        key = ""
        region = "ap-south-1"
        use_lockfile = true
    }
}
