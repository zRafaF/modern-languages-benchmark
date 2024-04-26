pub fn sort(mut vec: Vec<u8>) -> Vec<u8> {
    loop {
        let mut troca = false;
        for i in 0..vec.len() - 1 {
            let j = i + 1;
            if vec[i] > vec[j] {
                let a = vec[i];
                let b = vec[j];
                vec[i] = b;
                vec[j] = a;
                troca = true;
            }
        }
        if !troca {
            break;
        }
    }

    vec
}
