kubectl create ns perms

kubectl create serviceaccount testuser --namespace perms

Now you need to take the token and the ca.crt from secret of the serviceaccount testuser

Now apply thew rbac role in the namespace perms with kubectl apply -f test_role.yaml test_role_binding.yaml

kubectl config view > /tmp/testing_kube.cfg

Now edit /tmp/testing_kube.cfg and insert the token and the ca.crt

Now you can test if you have the permessions to work restrited inside namespace perms

kubectl --kubeconfig /tmp/testing_kube.cfg --context testing run nginx --image=nginx --replicas=1
